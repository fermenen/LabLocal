"""Vistas de analíticas y edad biológica (PhenoAge)."""
import json
from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView, DetailView, ListView, TemplateView

from django.utils.translation import gettext as _

from ..forms import AnalysisReportForm
from ..models import AnalysisReport, Biomarker, BiomarkerResult
from ..phenoage import update_report_phenoage


def _biomarkers_grouped():
    """Devuelve biomarcadores agrupados por categoría."""
    grupos = {}
    for bm in Biomarker.objects.all():
        cat = bm.get_category_display()
        grupos.setdefault(cat, []).append(bm)
    return grupos


def _save_biomarker_results(request, report):
    """Procesa los campos de biomarcador y crea/actualiza BiomarkerResult."""
    for bm in Biomarker.objects.all():
        raw = request.POST.get(f'biomarker_{bm.pk}_value', '').strip()
        if not raw:
            BiomarkerResult.objects.filter(report=report, biomarker=bm).delete()
            continue
        try:
            value = Decimal(raw.replace(',', '.'))
        except InvalidOperation:
            continue
        notes = request.POST.get(f'biomarker_{bm.pk}_notes', '').strip()
        BiomarkerResult.objects.update_or_create(
            report=report,
            biomarker=bm,
            defaults={'value': value, 'notes': notes},
        )


class ReportListView(LoginRequiredMixin, ListView):
    """Lista de todas las analíticas del usuario."""

    model = AnalysisReport
    template_name = 'labs/analysis/list.html'
    context_object_name = 'reports'

    def get_queryset(self):
        return AnalysisReport.objects.filter(user=self.request.user).prefetch_related('results')


class ReportCreateView(LoginRequiredMixin, View):
    """Crea una nueva analítica con sus valores de biomarcadores."""

    template_name = 'labs/analysis/form.html'

    def _back(self, request):
        """Devuelve la URL de retorno según el parámetro ?back=."""
        if request.GET.get('back') == 'dashboard':
            return 'dashboard'
        return None

    def get(self, request):
        return render(request, self.template_name, {
            'form': AnalysisReportForm(),
            'biomarkers_grouped': _biomarkers_grouped(),
            'existing_values': {},
            'action': 'Crear',
            'back': self._back(request),
        })

    def post(self, request):
        form = AnalysisReportForm(request.POST, request.FILES)
        back = self._back(request)
        if not form.is_valid():
            return render(request, self.template_name, {
                'form': form,
                'biomarkers_grouped': _biomarkers_grouped(),
                'existing_values': {},
                'action': 'Crear',
                'back': back,
            })
        report = form.save(commit=False)
        report.user = request.user
        report.save()
        _save_biomarker_results(request, report)
        update_report_phenoage(report)
        messages.success(request, _('Analysis "%(name)s" created successfully.') % {'name': report.name})
        if back == 'dashboard':
            return redirect('dashboard')
        return redirect('analysis_detail', pk=report.pk)


class ReportDetailView(LoginRequiredMixin, DetailView):
    """Detalle de una analítica con semáforo por biomarcador."""

    model = AnalysisReport
    template_name = 'labs/analysis/detail.html'
    context_object_name = 'report'

    def get_queryset(self):
        return AnalysisReport.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        results = self.object.results.select_related('biomarker').order_by(
            'biomarker__category', 'biomarker__order'
        )
        grupos = {}
        for result in results:
            cat = result.biomarker.get_category_display()
            grupos.setdefault(cat, []).append(result)
        ctx['results_grouped'] = grupos
        ctx['alerts'] = self.object.get_alerts()
        ctx['borderlines'] = self.object.get_borderlines()
        return ctx


class ReportUpdateView(LoginRequiredMixin, View):
    """Edita una analítica existente."""

    template_name = 'labs/analysis/form.html'

    def _get_report(self, request, pk):
        return get_object_or_404(AnalysisReport, pk=pk, user=request.user)

    def _existing_values(self, report):
        return {
            r.biomarker_id: {'value': str(r.value), 'notes': r.notes}
            for r in report.results.all()
        }

    def get(self, request, pk):
        report = self._get_report(request, pk)
        return render(request, self.template_name, {
            'form': AnalysisReportForm(instance=report),
            'biomarkers_grouped': _biomarkers_grouped(),
            'existing_values': self._existing_values(report),
            'report': report,
            'action': 'Editar',
        })

    def post(self, request, pk):
        report = self._get_report(request, pk)
        form = AnalysisReportForm(request.POST, instance=report)
        if not form.is_valid():
            return render(request, self.template_name, {
                'form': form,
                'biomarkers_grouped': _biomarkers_grouped(),
                'existing_values': self._existing_values(report),
                'report': report,
                'action': 'Editar',
            })
        report = form.save()
        _save_biomarker_results(request, report)
        update_report_phenoage(report)
        messages.success(request, _('Analysis "%(name)s" updated successfully.') % {'name': report.name})
        return redirect('analysis_detail', pk=report.pk)


class ReportDeleteView(LoginRequiredMixin, DeleteView):
    """Elimina una analítica tras confirmación."""

    model = AnalysisReport
    success_url = reverse_lazy('analysis_list')

    def get(self, request, *args, **kwargs):
        return redirect('analysis_detail', pk=self.get_object().pk)

    def get_queryset(self):
        return AnalysisReport.objects.filter(user=self.request.user)

    def form_valid(self, form):
        name = self.object.name
        response = super().form_valid(form)
        messages.success(self.request, _('Analysis "%(name)s" deleted successfully.') % {'name': name})
        return response


class PhenoAgeHistoryView(LoginRequiredMixin, TemplateView):
    """Historial de edad biológica y explicación del cálculo PhenoAge."""

    template_name = 'labs/phenoage/history.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        reports = AnalysisReport.objects.filter(user=self.request.user).order_by('date')
        profile = getattr(self.request.user, 'userprofile', None)
        birth_date = profile.birth_date if profile else None

        history, chart_labels, chart_values, chart_real_ages = [], [], [], []
        for report in reports:
            if report.phenoage_years is None:
                continue
            pheno = float(report.phenoage_years)
            diff = float(report.phenoage_delta_years or 0)
            history.append({'report': report, 'phenoage': pheno, 'diff': diff, 'younger': diff > 0})
            chart_labels.append(report.date.strftime('%d/%m/%Y'))
            chart_values.append(pheno)
            if birth_date:
                delta = report.date - birth_date
                chart_real_ages.append(round(delta.days / 365.25, 1))
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
