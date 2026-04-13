"""Vistas de perfil, familia y cuenta."""
from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView

from ..forms import FamilyUserCreateForm, UserProfileForm
from ..models import UserProfile

import json

User = get_user_model()


class ProfileView(LoginRequiredMixin, View):
    """Edición del perfil del usuario."""

    template_name = 'labs/profile/edit.html'

    def _get_profile(self, request):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        return profile

    def _get_context(self, request, form):
        return {
            'form': form,
            'all_users': User.objects.order_by('-is_superuser', 'username'),
        }

    def get(self, request):
        profile = self._get_profile(request)
        form = UserProfileForm(instance=profile, user=request.user)
        return render(request, self.template_name, self._get_context(request, form))

    def post(self, request):
        profile = self._get_profile(request)
        form = UserProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('profile')
        return render(request, self.template_name, self._get_context(request, form))


class FamilyUserCreateView(LoginRequiredMixin, View):
    """Crea una cuenta nueva para un miembro de la familia. Solo admin."""

    template_name = 'labs/profile/family_create.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(request, 'Solo el administrador puede crear cuentas.')
            return redirect('profile')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {'form': FamilyUserCreateForm()})

    def post(self, request):
        form = FamilyUserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Cuenta "{form.cleaned_data["username"]}" creada correctamente.')
            return redirect('profile')
        return render(request, self.template_name, {'form': form})


class PrivacyView(LoginRequiredMixin, TemplateView):
    """Página de política de privacidad."""

    template_name = 'labs/profile/privacy.html'


class PasswordChangeView(LoginRequiredMixin, View):
    """Cambio de contraseña del usuario autenticado."""

    template_name = 'labs/profile/password_change.html'

    def get(self, request):
        return render(request, self.template_name, {'form': PasswordChangeForm(request.user)})

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Contraseña actualizada correctamente.')
            return redirect('profile')
        return render(request, self.template_name, {'form': form})
