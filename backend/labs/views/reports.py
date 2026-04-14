"""Vistas de listado combinado y exportación de datos."""
import base64
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
    """Exporta todos los datos del usuario como JSON, sin datos identificativos."""

    def get(self, request):
        user = request.user

        # Profile — no identifying data (no name, username, email or date of birth)
        try:
            profile = user.userprofile
            profile_data = {
                'biological_sex': profile.biological_sex or None,
                'smoker': profile.smoker,
                'notes': profile.notes or None,
            }
        except UserProfile.DoesNotExist:
            profile_data = {}

        # Analysis reports
        analysis_qs = AnalysisReport.objects.filter(user=user).prefetch_related('results__biomarker')
        analysis = [
            {
                'name': r.name,
                'date': str(r.date),
                'lab': r.lab_name or None,
                'notes': r.notes or None,
                'phenoage_years': str(r.phenoage_years) if r.phenoage_years is not None else None,
                'phenoage_delta_years': str(r.phenoage_delta_years) if r.phenoage_delta_years is not None else None,
                'results': [
                    {
                        'biomarker': res.biomarker.name,
                        'loinc_code': res.biomarker.loinc_code or None,
                        'value': str(res.value),
                        'unit': res.biomarker.unit,
                        'status': res.status,
                        'notes': res.notes or None,
                    }
                    for res in r.results.all()
                ],
            }
            for r in analysis_qs
        ]

        # Body composition reports
        body_qs = BodyCompositionReport.objects.filter(user=user)
        body_composition = [
            {
                'name': r.name,
                'date': str(r.date),
                'notes': r.notes or None,
                'weight_kg': str(r.weight),
                'height_cm': str(r.height),
                'bmi': r.bmi,
                'body_fat_pct': str(r.body_fat_pct) if r.body_fat_pct is not None else None,
                'visceral_fat': str(r.visceral_fat) if r.visceral_fat is not None else None,
                'muscle_mass_kg': str(r.muscle_mass) if r.muscle_mass is not None else None,
                'water_pct': str(r.water_pct) if r.water_pct is not None else None,
                'protein_pct': str(r.protein_pct) if r.protein_pct is not None else None,
                'bone_mass_kg': str(r.bone_mass) if r.bone_mass is not None else None,
            }
            for r in body_qs
        ]

        # ECG reports — image as base64
        ecg_qs = ECGReport.objects.filter(user=user)
        ecgs = []
        for r in ecg_qs:
            image_b64 = None
            try:
                with r.image.open('rb') as f:
                    image_b64 = base64.b64encode(f.read()).decode('ascii')
            except Exception:
                pass
            ecgs.append({
                'name': r.name,
                'date': str(r.date),
                'notes': r.notes or None,
                'heart_rate_bpm': r.heart_rate,
                'image_base64': image_b64,
            })

        data = {
            'profile': profile_data,
            'analysis': analysis,
            'body_composition': body_composition,
            'ecg': ecgs,
        }

        response = HttpResponse(
            json.dumps(data, ensure_ascii=False, indent=2),
            content_type='application/json; charset=utf-8',
        )
        response['Content-Disposition'] = 'attachment; filename="lablocal_export.json"'
        return response
