"""Vista principal del dashboard."""
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from ..heart_rate import heart_rate_pct, heart_rate_scale, heart_rate_trend
from ..models import AnalysisReport, BodyCompositionReport, ECGReport
from ..pace import calcular_pace
from ..phenoage import get_phenoage_from_report


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

        latest_body = BodyCompositionReport.objects.filter(user=self.request.user).first()
        ctx['latest_body'] = latest_body
        if latest_body and latest_body.bmi:
            bmi = float(latest_body.bmi)
            ctx['bmi_pct'] = round(max(0, min(100, (bmi - 18) / 8 * 100)), 1)

        all_reports = list(reports)
        if len(all_reports) >= 2:
            pace_result = calcular_pace(all_reports[0], all_reports[1])
            ctx['pace_data'] = pace_result
            if pace_result['disponible']:
                pace = pace_result['pace']
                ctx['aging_ratio'] = pace
                ctx['aging_ratio_pct'] = round(max(0, min(100, pace / 2 * 100)), 1)
                ctx['aging_ratio_report'] = all_reports[0]
        else:
            ctx['pace_data'] = None

        analysis_recent = [
            {'obj': r, 'type': 'analysis', 'url': 'analysis_detail'}
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
