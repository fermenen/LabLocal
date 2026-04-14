"""Formularios de LabLocal."""
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import AnalysisReport, BodyCompositionReport, ECGReport, UserProfile

User = get_user_model()


class UserProfileForm(forms.ModelForm):
    """Formulario para editar el perfil del usuario."""

    first_name = forms.CharField(
        max_length=150, required=False, label=_('First name'),
        widget=forms.TextInput(attrs={'class': 'field'})
    )
    last_name = forms.CharField(
        max_length=150, required=False, label=_('Last name'),
        widget=forms.TextInput(attrs={'class': 'field'})
    )
    birth_date = forms.DateField(
        required=False, label=_('Date of birth'),
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'field'}, format='%Y-%m-%d'),
    )

    smoker = forms.TypedChoiceField(
        required=False,
        label=_('Smoker'),
        coerce=lambda x: None if x == '' else x == 'True',
        choices=[('', _('Not specified')), ('True', _('Yes')), ('False', _('No'))],
        widget=forms.Select(attrs={'class': 'field'}),
    )

    class Meta:
        model = UserProfile
        fields = ['avatar', 'birth_date', 'biological_sex', 'smoker', 'notes']
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'field', 'accept': 'image/*'}),
            'biological_sex': forms.Select(attrs={'class': 'field'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'field'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
        if self.instance and self.instance.pk:
            smoker_val = self.instance.smoker
            self.fields['smoker'].initial = '' if smoker_val is None else str(smoker_val)

    def save(self, commit=True):
        profile = super().save(commit=False)
        if self.user:
            self.user.first_name = self.cleaned_data['first_name']
            self.user.last_name = self.cleaned_data['last_name']
            self.user.save()
        if commit:
            profile.save()
        return profile


class AnalysisReportForm(forms.ModelForm):
    """Formulario para los metadatos de una analítica."""

    class Meta:
        model = AnalysisReport
        fields = ['name', 'date', 'lab_name', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'field',
                'placeholder': 'Ej: Reconocimiento laboral anual 2026',
            }),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'field'}, format='%Y-%m-%d'),
            'lab_name': forms.TextInput(attrs={
                'class': 'field',
                'placeholder': 'Ej: Clínica Salud Total',
            }),
            'notes': forms.Textarea(attrs={
                'rows': 3,
                'class': 'field',
                'placeholder': 'Observaciones adicionales...',
            }),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].input_formats = ['%Y-%m-%d']


class FamilyUserCreateForm(UserCreationForm):
    """Formulario para crear una cuenta de familiar."""

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'field'


class BodyCompositionForm(forms.ModelForm):
    """Formulario para registrar composición corporal."""

    class Meta:
        model = BodyCompositionReport
        fields = [
            'name', 'date',
            'weight', 'height',
            'body_fat_pct', 'visceral_fat',
            'muscle_mass', 'water_pct', 'protein_pct', 'bone_mass',
            'notes',
        ]
        widgets = {
            'name':          forms.TextInput(attrs={'class': 'field', 'placeholder': 'Ej: Báscula — enero 2026'}),
            'date':          forms.DateInput(attrs={'type': 'date', 'class': 'field'}, format='%Y-%m-%d'),
            'weight':        forms.NumberInput(attrs={'class': 'field', 'step': '0.1', 'placeholder': '70.5'}),
            'height':        forms.NumberInput(attrs={'class': 'field', 'step': '0.1', 'placeholder': '175.0'}),
            'body_fat_pct':  forms.NumberInput(attrs={'class': 'field', 'step': '0.1', 'placeholder': '18.5'}),
            'visceral_fat':  forms.NumberInput(attrs={'class': 'field', 'step': '0.1', 'placeholder': '8'}),
            'muscle_mass':   forms.NumberInput(attrs={'class': 'field', 'step': '0.1', 'placeholder': '35.0'}),
            'water_pct':     forms.NumberInput(attrs={'class': 'field', 'step': '0.1', 'placeholder': '58.0'}),
            'protein_pct':   forms.NumberInput(attrs={'class': 'field', 'step': '0.1', 'placeholder': '16.5'}),
            'bone_mass':     forms.NumberInput(attrs={'class': 'field', 'step': '0.1', 'placeholder': '3.2'}),
            'notes':         forms.Textarea(attrs={'class': 'field', 'rows': 2, 'placeholder': 'Observaciones...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].input_formats = ['%Y-%m-%d']


class ECGReportForm(forms.ModelForm):
    """Formulario para registrar electrocardiograma."""

    class Meta:
        model = ECGReport
        fields = ['name', 'date', 'image', 'heart_rate', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'field',
                'placeholder': 'Ej: ECG de rutina 2026',
            }),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'field'}, format='%Y-%m-%d'),
            'image': forms.FileInput(attrs={'class': 'field', 'accept': 'image/*'}),
            'heart_rate': forms.NumberInput(attrs={
                'class': 'field',
                'placeholder': 'Ej: 72',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'field',
                'rows': 2,
                'placeholder': 'Notas adicionales...',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].input_formats = ['%Y-%m-%d']
