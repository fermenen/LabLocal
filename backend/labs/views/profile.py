"""Vistas de perfil, familia y cuenta."""
import json
import os

import urllib.request
import urllib.error

from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView

from django.utils.translation import gettext as _

from ..forms import FamilyUserCreateForm, UserProfileForm
from ..models import AILicense, UserProfile

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
            'ai_license': AILicense.get_active(),
        }

    _REQUIRED_FIELDS = ('first_name', 'last_name', 'birth_date', 'biological_sex')

    def _apply_required(self, form):
        for field in self._REQUIRED_FIELDS:
            form.fields[field].required = True
        return form

    def get(self, request):
        profile = self._get_profile(request)
        form = self._apply_required(UserProfileForm(instance=profile, user=request.user))
        return render(request, self.template_name, self._get_context(request, form))

    def post(self, request):
        profile = self._get_profile(request)
        form = self._apply_required(
            UserProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        )
        if form.is_valid():
            form.save()
            messages.success(request, _('Profile updated successfully.'))
            return redirect('profile')
        return render(request, self.template_name, self._get_context(request, form))


class FamilyUserCreateView(LoginRequiredMixin, View):
    """Crea una cuenta nueva para un miembro de la familia. Solo admin."""

    template_name = 'labs/profile/family_create.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(request, _('Only the administrator can create accounts.'))
            return redirect('profile')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {'form': FamilyUserCreateForm()})

    def post(self, request):
        form = FamilyUserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Account "%(username)s" created successfully.') % {'username': form.cleaned_data['username']})
            return redirect('profile')
        return render(request, self.template_name, {'form': form})


class PrivacyView(LoginRequiredMixin, TemplateView):
    """Página de política de privacidad."""

    template_name = 'labs/profile/privacy.html'


class LanguageView(LoginRequiredMixin, TemplateView):
    """Página de selección de idioma."""

    template_name = 'labs/profile/language.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        flags = {'en': '🇬🇧', 'es': '🇪🇸', 'pt': '🇵🇹'}
        from django.conf import settings
        ctx['languages'] = [
            (code, name, flags.get(code, '🌐'))
            for code, name in settings.LANGUAGES
        ]
        return ctx


class LanguageChangeView(LoginRequiredMixin, View):
    """Cambia el idioma, añade mensaje de confirmación y redirige al perfil."""

    def post(self, request):
        from django.conf import settings as django_settings
        from django.utils import translation

        lang_code = request.POST.get('language', '')
        valid_codes = [code for code, _ in django_settings.LANGUAGES]

        if lang_code in valid_codes:
            translation.activate(lang_code)
            lang_name = dict(django_settings.LANGUAGES).get(lang_code, lang_code)
            messages.success(request, _('Language changed to %(lang)s.') % {'lang': lang_name})
            response = redirect('profile')
            response.set_cookie(
                django_settings.LANGUAGE_COOKIE_NAME,
                lang_code,
                max_age=django_settings.LANGUAGE_COOKIE_AGE,
                path=django_settings.LANGUAGE_COOKIE_PATH,
                domain=django_settings.LANGUAGE_COOKIE_DOMAIN,
                secure=django_settings.LANGUAGE_COOKIE_SECURE,
                httponly=django_settings.LANGUAGE_COOKIE_HTTPONLY,
                samesite=django_settings.LANGUAGE_COOKIE_SAMESITE,
            )
            return response

        return redirect('profile')


class AISubscribeView(LoginRequiredMixin, View):
    """El admin activa la licencia IA para toda la instalación."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(request, _('Only the administrator can activate the AI plan.'))
            return redirect('profile')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        if AILicense.get_active():
            messages.info(request, _('The AI license is already active for all users.'))
            return redirect('profile')

        ai_url = os.environ.get('LAB_LOCAL_AI_URL', '').rstrip('/')

        if not ai_url:
            messages.error(request, 'El servicio de IA no está configurado (LAB_LOCAL_AI_URL).')
            return redirect('profile')

        admin_profile, _ = UserProfile.objects.get_or_create(user=request.user)
        payload = json.dumps({
            'user_uuid': str(admin_profile.user_uuid),
            'plan': 'premium',
            'payment_ref': 'manual',
        }).encode('utf-8')

        req = urllib.request.Request(
            f'{ai_url}/api/licenses/activate',
            data=payload,
            headers={'Content-Type': 'application/json'},
            method='POST',
        )

        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode('utf-8'))
            AILicense.objects.create(
                api_key=data['api_key'],
                plan=data.get('plan', 'premium'),
                activated_by=request.user,
            )
            messages.success(request, _('AI Premium plan activated for all users!'))
        except urllib.error.HTTPError as e:
            body = e.read().decode('utf-8', errors='replace')
            messages.error(request, _('Error activating AI plan: %(code)s — %(body)s') % {'code': e.code, 'body': body[:200]})
        except Exception as e:
            messages.error(request, _('Could not connect to the AI service: %(error)s') % {'error': e})

        return redirect('profile')


class AIUnsubscribeView(LoginRequiredMixin, View):
    """Admin endpoint to cancel the global IA license for the installation."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(request, _('Only the administrator can cancel the AI license.'))
            return redirect('profile')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        active = AILicense.get_active()
        if not active:
            messages.info(request, _('There is no active AI license.'))
            return redirect('profile')

        ai_url = os.environ.get('LAB_LOCAL_AI_URL', '').rstrip('/')
        if not ai_url:
            messages.error(request, _('The AI service is not configured (LAB_LOCAL_AI_URL).'))
            return redirect('profile')

        admin_profile, _created = UserProfile.objects.get_or_create(user=request.user)
        req = urllib.request.Request(
            f'{ai_url}/api/licenses/deactivate',
            data=b'',
            headers={
                'X-API-Key': active.api_key,
                'X-User-UUID': str(admin_profile.user_uuid),
            },
            method='POST',
        )

        try:
            with urllib.request.urlopen(req, timeout=10):
                pass
        except urllib.error.HTTPError as e:
            body = e.read().decode('utf-8', errors='replace')
            messages.error(request, _('Error cancelling AI license: %(code)s — %(body)s') % {'code': e.code, 'body': body[:200]})
            return redirect('profile')
        except Exception as e:
            messages.error(request, _('Could not connect to the AI service: %(error)s') % {'error': e})
            return redirect('profile')

        try:
            active.delete()
            messages.success(request, _('AI license cancelled successfully.'))
        except Exception as e:
            messages.error(request, _('Error deleting local license: %(error)s') % {'error': e})

        return redirect('profile')


class PasswordChangeView(LoginRequiredMixin, View):
    """Cambio de contraseña del usuario autenticado."""

    template_name = 'labs/profile/password_change.html'

    def _style_form(self, form):
        for field in form.fields.values():
            field.widget.attrs['class'] = 'field'
        return form

    def get(self, request):
        return render(request, self.template_name, {'form': self._style_form(PasswordChangeForm(request.user))})

    def post(self, request):
        form = self._style_form(PasswordChangeForm(request.user, request.POST))
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, _('Password updated successfully.'))
            return redirect('profile')
        return render(request, self.template_name, {'form': form})
