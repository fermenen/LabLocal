"""Vistas del onboarding para nuevos usuarios."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from ..forms import AnalysisReportForm, UserProfileForm


class OnboardingProfileView(LoginRequiredMixin, FormView):
    """Paso 1 — rellenar datos del perfil.

    Si el usuario envía el formulario guardamos los datos y pasamos al paso 2.
    El botón "saltar" es un enlace GET al dashboard, no llega aquí.
    """

    template_name = 'labs/onboarding/profile.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('onboarding_analysis')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user.userprofile
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class OnboardingAnalysisView(LoginRequiredMixin, FormView):
    """Paso 2 — registrar una analítica inicial.

    Guardamos el registro de analítica (sin biomarcadores, se añaden luego)
    y redirigimos al dashboard.
    El botón "saltar" es un enlace GET al dashboard.
    """

    template_name = 'labs/onboarding/analysis.html'
    form_class = AnalysisReportForm
    success_url = reverse_lazy('dashboard')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['pdf'].required = True
        return form

    def form_valid(self, form):
        report = form.save(commit=False)
        report.user = self.request.user
        report.save()
        return super().form_valid(form)
