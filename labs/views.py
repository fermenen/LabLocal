"""Vistas de LabLocal — todas con LoginRequiredMixin."""
import json
from datetime import datetime
from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView, DetailView, ListView, TemplateView, UpdateView

from .forms import AnalysisReportForm, BodyCompositionForm, ECGReportForm, FamilyUserCreateForm, UserProfileForm
from .pace import calcular_pace

User = get_user_model()
from .models import AnalysisReport, Biomarker, BiomarkerResult, BodyCompositionReport, ECGReport, UserProfile
from .heart_rate import heart_rate_pct, heart_rate_scale, heart_rate_trend
from .phenoage import get_phenoage_from_report, update_report_phenoage


class DashboardView(LoginRequiredMixin, TemplateView):
    """Panel principal con resumen de la última analítica y alertas."""

    template_name = 'labs/dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        reports = AnalysisReport.objects.filter(user=self.request.user).prefetch_related(
            'results__biomarker'
        )
        latest = reports.first()
        ctx['latest_report'] = latest
        ctx['alerts'] = latest.get_alerts() if latest else []
        ctx['borderlines'] = latest.get_borderlines() if latest else []
        ctx['recent_reports'] = reports[:5]

        # Datos para el mosaico de marcadores
        if latest:
            all_results = list(latest.results.select_related('biomarker'))
            ctx['latest_results'] = all_results
            ctx['normal_count'] = sum(1 for r in all_results if r.status == 'normal')
            ctx['borderline_count'] = sum(1 for r in all_results if r.status == 'borderline')
            ctx['alert_count'] = sum(1 for r in all_results if r.status in ('low', 'high'))
        else:
            ctx['latest_results'] = []
            ctx['normal_count'] = 0
            ctx['borderline_count'] = 0
            ctx['alert_count'] = 0

        ctx['phenoage_data'] = get_phenoage_from_report(latest) if latest else None

        # Composición corporal — última medición
        latest_body = BodyCompositionReport.objects.filter(user=self.request.user).first()
        ctx['latest_body'] = latest_body
        if latest_body and latest_body.bmi:
            bmi = float(latest_body.bmi)
            # Rango de display: 18–26 (8 unidades)
            ctx['bmi_pct'] = round(max(0, min(100, (bmi - 18) / 8 * 100)), 1)

        # Ratio de envejecimiento — DunedinPACE aproximado (dos analíticas)
        all_reports = list(reports)
        if len(all_reports) >= 2:
            pace_result = calcular_pace(all_reports[0], all_reports[1])
            ctx['pace_data'] = pace_result
            if pace_result['disponible']:
                pace = pace_result['pace']
                ctx['aging_ratio'] = pace
                # Escala visual: pace 0.0–2.0 → 0–100%  (1.0 = 50 %)
                ctx['aging_ratio_pct'] = round(max(0, min(100, pace / 2 * 100)), 1)
                ctx['aging_ratio_report'] = all_reports[0]
        else:
            ctx['pace_data'] = None

        # Reportes recientes combinados (últimos 2 de todos los tipos)
        analysis_recent = [
            {'obj': r, 'type': 'analysis', 'url': 'report_detail'}
            for r in AnalysisReport.objects.filter(user=self.request.user)[:5]
        ]
        body_recent = [
            {'obj': r, 'type': 'body', 'url': 'body_detail'}
            for r in BodyCompositionReport.objects.filter(user=self.request.user)[:5]
        ]
        ecg_recent = [
            {'obj': r, 'type': 'ecg', 'url': 'ecg_detail'}
            for r in ECGReport.objects.filter(user=self.request.user)[:5]
        ]
        ctx['recent_all'] = sorted(
            analysis_recent + body_recent + ecg_recent,
            key=lambda x: (x['obj'].date, x['obj'].created_at),
            reverse=True,
        )[:2]

        # ECG — último registro y análisis de FC
        ecg_records = list(ECGReport.objects.filter(user=self.request.user).order_by('-date'))
        latest_ecg = ecg_records[0] if ecg_records else None
        ctx['latest_ecg'] = latest_ecg
        if latest_ecg and latest_ecg.heart_rate:
            ctx['ecg_hr_scale'] = heart_rate_scale(latest_ecg.heart_rate)
            ctx['ecg_hr_pct'] = heart_rate_pct(latest_ecg.heart_rate)
        ctx['ecg_hr_trend'] = heart_rate_trend(ecg_records)

        hour = datetime.now().hour
        if hour < 13:
            ctx['greeting'] = 'Buenos días'
        elif hour < 20:
            ctx['greeting'] = 'Buenas tardes'
        else:
            ctx['greeting'] = 'Buenas noches'

        return ctx


class ReportListView(LoginRequiredMixin, ListView):
    """Lista de todas las analíticas del usuario."""

    model = AnalysisReport
    template_name = 'labs/report_list.html'
    context_object_name = 'reports'

    def get_queryset(self):
        return AnalysisReport.objects.filter(user=self.request.user).prefetch_related('results')


class ReportCreateView(LoginRequiredMixin, View):
    """Crea una nueva analítica con sus valores de biomarcadores."""

    template_name = 'labs/report_form.html'

    def _get_biomarkers_grouped(self):
        """Devuelve biomarcadores agrupados por categoría."""
        biomarkers = Biomarker.objects.all()
        grupos = {}
        for bm in biomarkers:
            cat = bm.get_category_display()
            if cat not in grupos:
                grupos[cat] = []
            grupos[cat].append(bm)
        return grupos

    def get(self, request):
        from django.shortcuts import render
        form = AnalysisReportForm()
        return render(request, self.template_name, {
            'form': form,
            'biomarkers_grouped': self._get_biomarkers_grouped(),
            'existing_values': {},
            'action': 'Crear',
        })

    def post(self, request):
        from django.shortcuts import render
        form = AnalysisReportForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {
                'form': form,
                'biomarkers_grouped': self._get_biomarkers_grouped(),
                'existing_values': {},
                'action': 'Crear',
            })

        report = form.save(commit=False)
        report.user = request.user
        report.save()

        self._save_biomarker_results(request, report)
        update_report_phenoage(report)

        messages.success(request, f'Analítica «{report.name}» creada correctamente.')
        return redirect('report_detail', pk=report.pk)

    def _save_biomarker_results(self, request, report):
        """Procesa los campos de biomarcador y crea/actualiza BiomarkerResult."""
        biomarkers = Biomarker.objects.all()
        for bm in biomarkers:
            field_name = f'biomarker_{bm.pk}_value'
            raw = request.POST.get(field_name, '').strip()
            if not raw:
                BiomarkerResult.objects.filter(report=report, biomarker=bm).delete()
                continue
            try:
                value = Decimal(raw.replace(',', '.'))
            except InvalidOperation:
                continue
            notes_field = f'biomarker_{bm.pk}_notes'
            notes = request.POST.get(notes_field, '').strip()
            BiomarkerResult.objects.update_or_create(
                report=report,
                biomarker=bm,
                defaults={'value': value, 'notes': notes},
            )


class ReportDetailView(LoginRequiredMixin, DetailView):
    """Detalle de una analítica con semáforo por biomarcador."""

    model = AnalysisReport
    template_name = 'labs/report_detail.html'
    context_object_name = 'report'

    def get_queryset(self):
        return AnalysisReport.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        results = self.object.results.select_related('biomarker').order_by(
            'biomarker__category', 'biomarker__order'
        )
        # Agrupar por categoría
        grupos = {}
        for result in results:
            cat = result.biomarker.get_category_display()
            if cat not in grupos:
                grupos[cat] = []
            grupos[cat].append(result)
        ctx['results_grouped'] = grupos
        ctx['alerts'] = self.object.get_alerts()
        ctx['borderlines'] = self.object.get_borderlines()
        return ctx


class ReportUpdateView(LoginRequiredMixin, View):
    """Edita una analítica existente."""

    template_name = 'labs/report_form.html'

    def _get_biomarkers_grouped(self):
        biomarkers = Biomarker.objects.all()
        grupos = {}
        for bm in biomarkers:
            cat = bm.get_category_display()
            if cat not in grupos:
                grupos[cat] = []
            grupos[cat].append(bm)
        return grupos

    def _get_report(self, request, pk):
        return get_object_or_404(AnalysisReport, pk=pk, user=request.user)

    def _existing_values(self, report):
        return {
            r.biomarker_id: {'value': str(r.value), 'notes': r.notes}
            for r in report.results.all()
        }

    def get(self, request, pk):
        from django.shortcuts import render
        report = self._get_report(request, pk)
        form = AnalysisReportForm(instance=report)
        return render(request, self.template_name, {
            'form': form,
            'biomarkers_grouped': self._get_biomarkers_grouped(),
            'existing_values': self._existing_values(report),
            'report': report,
            'action': 'Editar',
        })

    def post(self, request, pk):
        from django.shortcuts import render
        report = self._get_report(request, pk)
        form = AnalysisReportForm(request.POST, instance=report)
        if not form.is_valid():
            return render(request, self.template_name, {
                'form': form,
                'biomarkers_grouped': self._get_biomarkers_grouped(),
                'existing_values': self._existing_values(report),
                'report': report,
                'action': 'Editar',
            })

        report = form.save()
        self._save_biomarker_results(request, report)
        update_report_phenoage(report)

        messages.success(request, f'Analítica «{report.name}» actualizada correctamente.')
        return redirect('report_detail', pk=report.pk)


class PhenoAgeHistoryView(LoginRequiredMixin, TemplateView):
    """Historial de edad biológica y explicación del cálculo PhenoAge."""

    template_name = 'labs/phenoage_history.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        reports = (
            AnalysisReport.objects
            .filter(user=self.request.user)
            .order_by('date')
        )

        profile = getattr(self.request.user, 'userprofile', None)
        birth_date = profile.birth_date if profile else None

        history = []
        chart_labels = []
        chart_values = []
        chart_real_ages = []
        for report in reports:
            if report.phenoage_years is None:
                continue
            pheno = float(report.phenoage_years)
            diff = float(report.phenoage_delta_years or 0)
            history.append({
                'report': report,
                'phenoage': pheno,
                'diff': diff,
                'younger': diff > 0,
            })
            chart_labels.append(report.date.strftime('%d/%m/%Y'))
            chart_values.append(pheno)
            if birth_date:
                delta = report.date - birth_date
                real_age = round(delta.days / 365.25, 1)
                chart_real_ages.append(real_age)
            else:
                chart_real_ages.append(None)

        ctx['history'] = history
        ctx['chart_data'] = json.dumps({
            'labels': chart_labels,
            'values': chart_values,
            'real_ages': chart_real_ages,
        })
        ctx['latest_report'] = reports.last() if reports else None
        return ctx

    def _save_biomarker_results(self, request, report):
        biomarkers = Biomarker.objects.all()
        for bm in biomarkers:
            field_name = f'biomarker_{bm.pk}_value'
            raw = request.POST.get(field_name, '').strip()
            if not raw:
                BiomarkerResult.objects.filter(report=report, biomarker=bm).delete()
                continue
            try:
                value = Decimal(raw.replace(',', '.'))
            except InvalidOperation:
                continue
            notes_field = f'biomarker_{bm.pk}_notes'
            notes = request.POST.get(notes_field, '').strip()
            BiomarkerResult.objects.update_or_create(
                report=report,
                biomarker=bm,
                defaults={'value': value, 'notes': notes},
            )


class ReportDeleteView(LoginRequiredMixin, DeleteView):
    """Elimina una analítica tras confirmación."""

    model = AnalysisReport
    template_name = 'labs/report_confirm_delete.html'
    success_url = reverse_lazy('report_list')

    def get_queryset(self):
        return AnalysisReport.objects.filter(user=self.request.user)

    def form_valid(self, form):
        name = self.object.name
        response = super().form_valid(form)
        messages.success(self.request, f'Analítica «{name}» eliminada correctamente.')
        return response


class BiomarkerListView(LoginRequiredMixin, ListView):
    """Catálogo de biomarcadores agrupados por categoría."""

    model = Biomarker
    template_name = 'labs/biomarker_list.html'
    context_object_name = 'biomarkers'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        grupos = {}
        for bm in ctx['biomarkers']:
            cat = bm.get_category_display()
            if cat not in grupos:
                grupos[cat] = []
            grupos[cat].append(bm)
        ctx['biomarkers_grouped'] = grupos
        return ctx


class BiomarkerDetailView(LoginRequiredMixin, DetailView):
    """Detalle de un biomarcador con gráfico histórico."""

    model = Biomarker
    template_name = 'labs/biomarker_detail.html'
    context_object_name = 'biomarker'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # Historial del usuario para este biomarcador
        results = (
            BiomarkerResult.objects
            .filter(report__user=self.request.user, biomarker=self.object)
            .select_related('report')
            .order_by('report__date')
        )
        ctx['results'] = results

        # Datos para Chart.js
        try:
            sex = self.request.user.userprofile.biological_sex
        except UserProfile.DoesNotExist:
            sex = ''
        ref_min, ref_max = self.object.get_ref_range(sex)

        chart_labels = [r.report.date.strftime('%d/%m/%Y') for r in results]
        chart_values = [float(r.value) for r in results]
        ctx['chart_data'] = json.dumps({
            'labels': chart_labels,
            'values': chart_values,
            'ref_min': float(ref_min) if ref_min is not None else None,
            'ref_max': float(ref_max) if ref_max is not None else None,
            'unit': self.object.unit,
        })
        return ctx


class ProfileView(LoginRequiredMixin, View):
    """Edición del perfil del usuario."""

    template_name = 'labs/profile.html'

    def _get_profile(self, request):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        return profile

    def _get_context(self, request, form):
        return {
            'form': form,
            'all_users': User.objects.order_by('-is_superuser', 'username'),
        }

    def get(self, request):
        from django.shortcuts import render
        profile = self._get_profile(request)
        form = UserProfileForm(instance=profile, user=request.user)
        return render(request, self.template_name, self._get_context(request, form))

    def post(self, request):
        from django.shortcuts import render
        profile = self._get_profile(request)
        form = UserProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('profile')
        return render(request, self.template_name, self._get_context(request, form))


class BodyCompositionListView(LoginRequiredMixin, ListView):
    """Lista de registros de composición corporal del usuario con gráfica de evolución de IMC."""

    model = BodyCompositionReport
    template_name = 'labs/body/list.html'
    context_object_name = 'records'

    def get_queryset(self):
        return BodyCompositionReport.objects.filter(user=self.request.user).order_by('-date')

    def get_context_data(self, **kwargs):
        import json
        ctx = super().get_context_data(**kwargs)
        all_ordered = sorted(ctx['records'], key=lambda r: r.date)

        records_with_bmi = [r for r in all_ordered if r.bmi is not None]
        if records_with_bmi:
            ctx['chart_data'] = json.dumps({
                'labels': [r.date.strftime('%d/%m/%Y') for r in records_with_bmi],
                'values': [r.bmi for r in records_with_bmi],
            })

        # Gráfica de envejecimiento: grasa corporal y masa muscular en el tiempo
        aging_records = [r for r in all_ordered if r.body_fat_pct is not None or r.muscle_mass is not None]
        if aging_records:
            labels = [r.date.strftime('%d/%m/%Y') for r in aging_records]
            ctx['aging_chart_data'] = json.dumps({
                'labels': labels,
                'fat': [float(r.body_fat_pct) if r.body_fat_pct is not None else None for r in aging_records],
                'muscle': [float(r.muscle_mass) if r.muscle_mass is not None else None for r in aging_records],
                'has_fat': any(r.body_fat_pct is not None for r in aging_records),
                'has_muscle': any(r.muscle_mass is not None for r in aging_records),
            })
        return ctx


class BodyCompositionCreateView(LoginRequiredMixin, View):
    """Crea un nuevo registro de composición corporal."""

    template_name = 'labs/body/form.html'

    def get(self, request):
        from django.shortcuts import render
        return render(request, self.template_name, {'form': BodyCompositionForm(), 'editing': False})

    def post(self, request):
        from django.shortcuts import render
        form = BodyCompositionForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.user = request.user
            record.save()
            messages.success(request, 'Registro guardado correctamente.')
            return redirect('body_detail', pk=record.pk)
        return render(request, self.template_name, {'form': form, 'editing': False})


class BodyCompositionDetailView(LoginRequiredMixin, DetailView):
    """Detalle de un registro de composición corporal."""

    model = BodyCompositionReport
    template_name = 'labs/body/detail.html'
    context_object_name = 'record'

    def get_queryset(self):
        return BodyCompositionReport.objects.filter(user=self.request.user)


class BodyCompositionUpdateView(LoginRequiredMixin, View):
    """Edita un registro de composición corporal."""

    template_name = 'labs/body/form.html'

    def _get_record(self, request, pk):
        return get_object_or_404(BodyCompositionReport, pk=pk, user=request.user)

    def get(self, request, pk):
        from django.shortcuts import render
        record = self._get_record(request, pk)
        return render(request, self.template_name, {'form': BodyCompositionForm(instance=record), 'record': record, 'editing': True})

    def post(self, request, pk):
        from django.shortcuts import render
        record = self._get_record(request, pk)
        form = BodyCompositionForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro actualizado correctamente.')
            return redirect('body_detail', pk=record.pk)
        return render(request, self.template_name, {'form': form, 'record': record, 'editing': True})


class BodyCompositionDeleteView(LoginRequiredMixin, DeleteView):
    """Elimina un registro de composición corporal (solo acepta POST; GET redirige al detalle)."""

    model = BodyCompositionReport
    success_url = reverse_lazy('body_list')
    context_object_name = 'record'

    def get_queryset(self):
        return BodyCompositionReport.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        record = self.get_object()
        return redirect('body_detail', pk=record.pk)


class ECGListView(LoginRequiredMixin, ListView):
    """Lista de electrocardiogramas del usuario con gráfica de evolución de FC."""

    model = ECGReport
    template_name = 'labs/ecg/list.html'
    context_object_name = 'records'

    def get_queryset(self):
        return ECGReport.objects.filter(user=self.request.user).order_by('-date')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        records_with_hr = [r for r in ctx['records'] if r.heart_rate]
        if records_with_hr:
            ordered = sorted(records_with_hr, key=lambda r: r.date)
            import json
            ctx['chart_data'] = json.dumps({
                'labels': [r.date.strftime('%d/%m/%Y') for r in ordered],
                'values': [r.heart_rate for r in ordered],
            })
            ctx['ecg_hr_trend'] = heart_rate_trend(ordered[::-1])
        return ctx


class ECGCreateView(LoginRequiredMixin, View):
    """Crea un nuevo electrocardiograma."""

    template_name = 'labs/ecg/form.html'

    def get(self, request):
        from django.shortcuts import render
        return render(request, self.template_name, {'form': ECGReportForm(), 'editing': False})

    def post(self, request):
        from django.shortcuts import render
        form = ECGReportForm(request.POST, request.FILES)
        if form.is_valid():
            record = form.save(commit=False)
            record.user = request.user
            record.save()
            messages.success(request, 'Electrocardiograma guardado correctamente.')
            return redirect('ecg_detail', pk=record.pk)
        return render(request, self.template_name, {'form': form, 'editing': False})


class ECGDetailView(LoginRequiredMixin, DetailView):
    """Detalle de un electrocardiograma."""

    model = ECGReport
    template_name = 'labs/ecg/detail.html'
    context_object_name = 'record'

    def get_queryset(self):
        return ECGReport.objects.filter(user=self.request.user)


class ECGUpdateView(LoginRequiredMixin, View):
    """Edita un electrocardiograma."""

    template_name = 'labs/ecg/form.html'

    def _get_record(self, request, pk):
        return get_object_or_404(ECGReport, pk=pk, user=request.user)

    def get(self, request, pk):
        from django.shortcuts import render
        record = self._get_record(request, pk)
        return render(request, self.template_name, {'form': ECGReportForm(instance=record), 'record': record, 'editing': True})

    def post(self, request, pk):
        from django.shortcuts import render
        record = self._get_record(request, pk)
        form = ECGReportForm(request.POST, request.FILES, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Electrocardiograma actualizado correctamente.')
            return redirect('ecg_detail', pk=record.pk)
        return render(request, self.template_name, {'form': form, 'record': record, 'editing': True})


class ECGDeleteView(LoginRequiredMixin, DeleteView):
    """Elimina un electrocardiograma (solo acepta POST; GET redirige al detalle)."""

    model = ECGReport
    success_url = reverse_lazy('ecg_list')
    context_object_name = 'record'

    def get_queryset(self):
        return ECGReport.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        record = self.get_object()
        return redirect('ecg_detail', pk=record.pk)


class AllReportsView(LoginRequiredMixin, TemplateView):
    """Lista combinada de todos los registros (analíticas, composición, ECG)."""

    template_name = 'labs/reports_all.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user

        analysis = [
            {'obj': r, 'type': 'analysis', 'url': 'report_detail'}
            for r in AnalysisReport.objects.filter(user=user)
        ]
        body = [
            {'obj': r, 'type': 'body', 'url': 'body_detail'}
            for r in BodyCompositionReport.objects.filter(user=user)
        ]
        ecg = [
            {'obj': r, 'type': 'ecg', 'url': 'ecg_detail'}
            for r in ECGReport.objects.filter(user=user)
        ]

        all_records = sorted(
            analysis + body + ecg,
            key=lambda x: (x['obj'].date, x['obj'].created_at),
            reverse=True,
        )
        ctx['records'] = all_records
        return ctx


class FamilyUserCreateView(LoginRequiredMixin, View):
    """Crea una cuenta nueva para un miembro de la familia. Solo admin."""

    template_name = 'labs/family_create.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(request, 'Solo el administrador puede crear cuentas.')
            return redirect('profile')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        from django.shortcuts import render
        return render(request, self.template_name, {'form': FamilyUserCreateForm()})

    def post(self, request):
        from django.shortcuts import render
        form = FamilyUserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Cuenta "{form.cleaned_data["username"]}" creada correctamente.')
            return redirect('profile')
        return render(request, self.template_name, {'form': form})


class ExportView(LoginRequiredMixin, View):
    """Exporta todos los datos del usuario como JSON."""

    def get(self, request):
        reports = AnalysisReport.objects.filter(user=request.user).prefetch_related(
            'results__biomarker'
        )

        try:
            profile = request.user.userprofile
            perfil_data = {
                'birth_date': str(profile.birth_date) if profile.birth_date else None,
                'biological_sex': profile.biological_sex,
                'notes': profile.notes,
            }
        except UserProfile.DoesNotExist:
            perfil_data = {}

        data = {
            'usuario': request.user.username,
            'perfil': perfil_data,
            'analiticas': [
                {
                    'id': r.pk,
                    'nombre': r.name,
                    'fecha': str(r.date),
                    'laboratorio': r.lab_name,
                    'notas': r.notes,
                    'resultados': [
                        {
                            'biomarcador': res.biomarker.name,
                            'codigo_loinc': res.biomarker.loinc_code,
                            'valor': str(res.value),
                            'unidad': res.biomarker.unit,
                            'estado': res.status,
                            'notas': res.notes,
                        }
                        for res in r.results.all()
                    ],
                }
                for r in reports
            ],
        }

        response = HttpResponse(
            json.dumps(data, ensure_ascii=False, indent=2),
            content_type='application/json; charset=utf-8',
        )
        response['Content-Disposition'] = 'attachment; filename="lablocal_export.json"'
        return response


def custom_404(request, exception):
    """Redirige a home con mensaje de aviso en lugar de mostrar la página 404."""
    messages.warning(request, 'No hemos encontrado la página que buscas.')
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')
