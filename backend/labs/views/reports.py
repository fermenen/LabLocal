"""Vistas de listado combinado y exportación de datos."""
import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView

from ..models import AnalysisReport, BodyCompositionReport, ECGReport, UserProfile


class AllReportsView(LoginRequiredMixin, TemplateView):
    """Lista combinada de todos los registros (analíticas, composición, ECG)."""

    template_name = 'labs/reports/all.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user

        analysis = [{'obj': r, 'type': 'analysis', 'url': 'analysis_detail'}
                    for r in AnalysisReport.objects.filter(user=user)]
        body = [{'obj': r, 'type': 'body', 'url': 'body_detail'}
                for r in BodyCompositionReport.objects.filter(user=user)]
        ecg = [{'obj': r, 'type': 'ecg', 'url': 'ecg_detail'}
               for r in ECGReport.objects.filter(user=user)]

        ctx['records'] = sorted(
            analysis + body + ecg,
            key=lambda x: (x['obj'].date, x['obj'].created_at),
            reverse=True,
        )
        return ctx


class ExportView(LoginRequiredMixin, View):
    """Exporta todos los datos del usuario como JSON."""

    def get(self, request):
        reports = AnalysisReport.objects.filter(user=request.user).prefetch_related('results__biomarker')

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
