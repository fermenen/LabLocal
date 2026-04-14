"""Vistas de autenticación y utilidades generales."""
from django.contrib import messages
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth.views import LogoutView as AuthLogoutView
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _


class LoginView(AuthLoginView):
    """Login con mensaje de bienvenida al entrar.

    En el primer login (last_login is None) redirige al onboarding
    en vez de al dashboard.
    """

    template_name = 'labs/login.html'

    def form_valid(self, form):
        user = form.get_user()
        # Guardamos ANTES de llamar a super(), que es cuando Django actualiza last_login.
        self._is_first_login = user.last_login is None
        if not self._is_first_login:
            messages.success(
                self.request,
                _('Welcome back, %(name)s.') % {'name': user.get_short_name() or user.username},
            )
        return super().form_valid(form)

    def get_success_url(self):
        if getattr(self, '_is_first_login', False):
            return str(reverse_lazy('onboarding_profile'))
        return super().get_success_url()


class LogoutView(AuthLogoutView):
    """Logout con mensaje de confirmación."""

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, _('You have been signed out.'))
        return super().dispatch(request, *args, **kwargs)


def health_check(request):
    """Endpoint liviano para comprobar disponibilidad del servidor."""
    return JsonResponse({'ok': True})


def custom_404(request, exception):
    """Redirige a home con mensaje de aviso en lugar de mostrar la página 404."""
    messages.warning(request, _('The page you requested was not found.'))
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')
