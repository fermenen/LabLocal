"""Vistas del catálogo de biomarcadores."""
import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView

from ..models import Biomarker, BiomarkerResult, UserProfile


class BiomarkerListView(LoginRequiredMixin, ListView):
    """Catálogo de biomarcadores agrupados por categoría."""

    model = Biomarker
    template_name = 'labs/biomarkers/list.html'
    context_object_name = 'biomarkers'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        grupos = {}
        for bm in ctx['biomarkers']:
            cat = bm.get_category_display()
            grupos.setdefault(cat, []).append(bm)
        ctx['biomarkers_grouped'] = grupos
        return ctx


class BiomarkerDetailView(LoginRequiredMixin, DetailView):
    """Detalle de un biomarcador con gráfico histórico."""

    model = Biomarker
    template_name = 'labs/biomarkers/detail.html'
    context_object_name = 'biomarker'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        results = (
            BiomarkerResult.objects
            .filter(report__user=self.request.user, biomarker=self.object)
            .select_related('report')
            .order_by('report__date')
        )
        ctx['results'] = results

        try:
            sex = self.request.user.userprofile.biological_sex
        except UserProfile.DoesNotExist:
            sex = ''
        ref_min, ref_max = self.object.get_ref_range(sex)

        ctx['chart_data'] = json.dumps({
            'labels': [r.report.date.strftime('%d/%m/%Y') for r in results],
            'values': [float(r.value) for r in results],
            'ref_min': float(ref_min) if ref_min is not None else None,
            'ref_max': float(ref_max) if ref_max is not None else None,
            'unit': self.object.unit,
        })
        return ctx
