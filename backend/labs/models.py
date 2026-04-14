"""Modelos de datos de LabLocal."""
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _



class UserProfile(models.Model):
    """Perfil extendido del usuario con datos médicos básicos."""
    def avatar_upload_path(_instance, filename):
        ext = filename.split('.')[-1]
        return f'avatars/{uuid.uuid4()}.{ext}'

    SEXO_CHOICES = [('M', _('Male')), ('F', _('Female'))]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    user_uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        db_index=True,
        verbose_name=_('Public UUID')
    )
    avatar = models.ImageField(
        upload_to=avatar_upload_path,
        null=True, blank=True, verbose_name=_('Profile picture')
    )
    birth_date = models.DateField(null=True, blank=True, verbose_name=_('Date of birth'))
    biological_sex = models.CharField(
        max_length=1, choices=SEXO_CHOICES, blank=True, verbose_name=_('Biological sex')
    )
    smoker = models.BooleanField(null=True, blank=True, verbose_name=_('Smoker'))
    notes = models.TextField(blank=True, verbose_name=_('Notes'))

    class Meta:
        verbose_name = _('User profile')
        verbose_name_plural = _('User profiles')

    def __str__(self):
        return f'Perfil de {self.user.username}'


@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    """Crea automáticamente un UserProfile al crear un User."""
    if created:
        UserProfile.objects.get_or_create(user=instance)


class Biomarker(models.Model):
    """Catálogo de biomarcadores médicos."""

    CATEGORIA_CHOICES = [
        ('HEMATOLOGIA', _('Hematology')),
        ('BIOQUIMICA', _('Biochemistry')),
        ('LIPIDOS', _('Lipids')),
        ('TIROIDES', _('Thyroid')),
        ('HIERRO', _('Iron')),
        ('INFLAMACION', _('Inflammation')),
        ('ORINA', _('Urine')),
        ('VITAMINAS', _('Vitamins')),
        ('OTRO', _('Other')),
    ]

    loinc_code = models.CharField(max_length=30, unique=True, verbose_name=_('LOINC code'))
    category = models.CharField(
        max_length=20, choices=CATEGORIA_CHOICES, default='OTRO', verbose_name=_('Category')
    )
    unit = models.CharField(max_length=50, verbose_name=_('Unit'))
    ref_min_male = models.DecimalField(
        max_digits=10, decimal_places=3, null=True, blank=True,
        verbose_name=_('Reference min (male)')
    )
    ref_max_male = models.DecimalField(
        max_digits=10, decimal_places=3, null=True, blank=True,
        verbose_name=_('Reference max (male)')
    )
    ref_min_female = models.DecimalField(
        max_digits=10, decimal_places=3, null=True, blank=True,
        verbose_name=_('Reference min (female)')
    )
    ref_max_female = models.DecimalField(
        max_digits=10, decimal_places=3, null=True, blank=True,
        verbose_name=_('Reference max (female)')
    )
    low_is_bad = models.BooleanField(
        default=True, verbose_name=_('Low value is bad')
    )
    order = models.PositiveIntegerField(default=0, verbose_name=_('Order'))

    class Meta:
        verbose_name = _('Biomarker')
        verbose_name_plural = _('Biomarkers')
        ordering = ['category', 'order']

    # ------------------------------------------------------------------
    # Translated properties (text lives in biomarker_i18n.py, not in DB)
    # ------------------------------------------------------------------

    @property
    def name(self):
        from labs.biomarker_i18n import get_biomarker_field
        return get_biomarker_field(self.loinc_code, 'name')

    @property
    def short_name(self):
        from labs.biomarker_i18n import get_biomarker_field
        return get_biomarker_field(self.loinc_code, 'short_name')

    @property
    def description(self):
        from labs.biomarker_i18n import get_biomarker_field
        return get_biomarker_field(self.loinc_code, 'description')

    def __str__(self):
        return f'{self.name} ({self.unit})'

    def get_ref_range(self, sex):
        """Devuelve (ref_min, ref_max) según el sexo biológico."""
        if sex == 'M':
            return self.ref_min_male, self.ref_max_male
        return self.ref_min_female, self.ref_max_female


class BaseReport(models.Model):
    """Clase base abstracta para todos los tipos de registros de salud."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='%(class)s_reports', verbose_name=_('User')
    )
    name = models.CharField(max_length=200, verbose_name=_('Name'))
    date = models.DateField(verbose_name=_('Date'))
    notes = models.TextField(blank=True, verbose_name=_('Notes'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))

    class Meta:
        abstract = True
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f'{self.name} — {self.date}'


class AnalysisReport(BaseReport):
    """Analítica o reconocimiento médico completo."""

    lab_name = models.CharField(max_length=200, blank=True, verbose_name=_('Laboratory'))
    phenoage_years = models.DecimalField(
        max_digits=5, decimal_places=1, null=True, blank=True,
        verbose_name=_('Biological age (PhenoAge)')
    )
    phenoage_delta_years = models.DecimalField(
        max_digits=5, decimal_places=1, null=True, blank=True,
        verbose_name=_('Biological-chronological age difference')
    )
    phenoage_missing = models.TextField(
        blank=True, default='',
        verbose_name=_('Missing markers for PhenoAge')
    )

    class Meta(BaseReport.Meta):
        verbose_name = _('Analysis')
        verbose_name_plural = _('Analyses')

    def get_alerts(self):
        """Devuelve los resultados fuera de rango normal."""
        return [r for r in self.results.select_related('biomarker') if r.status in ('low', 'high')]

    def get_borderlines(self):
        """Devuelve los resultados en límite."""
        return [r for r in self.results.select_related('biomarker') if r.status == 'borderline']


class BodyCompositionReport(BaseReport):
    """Registro de composición corporal (báscula inteligente o medición manual)."""

    weight = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name=_('Weight (kg)')
    )
    height = models.DecimalField(
        max_digits=5, decimal_places=1, verbose_name=_('Height (cm)')
    )
    body_fat_pct = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        verbose_name=_('Body fat (%)')
    )
    visceral_fat = models.DecimalField(
        max_digits=5, decimal_places=1, null=True, blank=True,
        verbose_name=_('Visceral fat (level)')
    )
    muscle_mass = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        verbose_name=_('Muscle mass (kg)')
    )
    water_pct = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        verbose_name=_('Water (%)')
    )
    protein_pct = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        verbose_name=_('Protein (%)')
    )
    bone_mass = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        verbose_name=_('Bone mass (kg)')
    )

    class Meta(BaseReport.Meta):
        verbose_name = _('Body composition')
        verbose_name_plural = _('Body compositions')

    @property
    def bmi(self):
        """IMC calculado: peso(kg) / altura(m)²"""
        if not self.weight or not self.height or self.height == 0:
            return None
        height_m = float(self.height) / 100
        return round(float(self.weight) / (height_m ** 2), 1)

    @property
    def bmi_status(self):
        """Categoría del IMC según OMS. Retorna (etiqueta, color_key)."""
        bmi = self.bmi
        if bmi is None:
            return (_('No data'), 'unknown')
        if bmi < 18.5:
            return (_('Underweight'), 'low')
        if bmi < 25.0:
            return (_('Normal'), 'normal')
        if bmi < 30.0:
            return (_('Overweight'), 'borderline')
        return (_('Obesity'), 'high')



class ECGReport(BaseReport):
    """Registro de electrocardiograma (ECG/EKG)."""
    def ecg_image_upload_path(_instance, filename):
        ext = filename.split('.')[-1]
        return f'ecg/{uuid.uuid4()}.{ext}'

    image = models.ImageField(
        upload_to=ecg_image_upload_path,
        verbose_name=_('ECG image')
    )
    heart_rate = models.PositiveIntegerField(
        null=True, blank=True, verbose_name=_('Heart rate (bpm)')
    )

    class Meta(BaseReport.Meta):
        verbose_name = _('Electrocardiogram')
        verbose_name_plural = _('Electrocardiograms')

    def __str__(self):
        return f'ECG — {self.name} ({self.date})'


class BiomarkerResult(models.Model):
    """Valor de un biomarcador en una analítica concreta."""

    report = models.ForeignKey(
        AnalysisReport, on_delete=models.CASCADE, related_name='results', verbose_name=_('Analysis')
    )
    biomarker = models.ForeignKey(
        Biomarker, on_delete=models.PROTECT, related_name='results', verbose_name=_('Biomarker')
    )
    value = models.DecimalField(max_digits=12, decimal_places=4, verbose_name=_('Value'))
    notes = models.TextField(blank=True, verbose_name=_('Notes'))

    class Meta:
        verbose_name = _('Result')
        verbose_name_plural = _('Results')
        unique_together = [('report', 'biomarker')]
        ordering = ['biomarker__category', 'biomarker__order']

    def __str__(self):
        return f'{self.biomarker.short_name}: {self.value} {self.biomarker.unit}'

    @property
    def status(self):
        """
        Calcula el semáforo del resultado según el rango de referencia del sexo del usuario.
        Retorna: 'normal' | 'borderline' | 'low' | 'high' | 'unknown'
        """
        try:
            sex = self.report.user.userprofile.biological_sex
        except UserProfile.DoesNotExist:
            return 'unknown'

        ref_min, ref_max = self.biomarker.get_ref_range(sex)

        if ref_min is None and ref_max is None:
            return 'unknown'

        val = float(self.value)
        rmin = float(ref_min) if ref_min is not None else None
        rmax = float(ref_max) if ref_max is not None else None

        # Dentro del rango
        if rmin is not None and rmax is not None:
            if rmin <= val <= rmax:
                return 'normal'
            rango = rmax - rmin if rmax > rmin else rmax
            if val < rmin:
                desviacion = (rmin - val) / rango if rango > 0 else 1
                return 'borderline' if desviacion <= 0.15 else 'low'
            else:
                desviacion = (val - rmax) / rango if rango > 0 else 1
                return 'borderline' if desviacion <= 0.15 else 'high'

        if rmax is not None:
            if val <= rmax:
                return 'normal'
            desviacion = (val - rmax) / rmax if rmax > 0 else 1
            return 'borderline' if desviacion <= 0.15 else 'high'

        # Solo rmin
        if val >= rmin:
            return 'normal'
        desviacion = (rmin - val) / rmin if rmin > 0 else 1
        return 'borderline' if desviacion <= 0.15 else 'low'

    @property
    def status_display(self):
        """Texto legible del semáforo."""
        return {
            'normal': _('Normal'),
            'borderline': _('Borderline'),
            'low': _('Low'),
            'high': _('High'),
            'unknown': _('No range'),
        }.get(self.status, _('Unknown'))

    @property
    def status_color(self):
        """Clase CSS de color según el semáforo."""
        return {
            'normal': 'green',
            'borderline': 'yellow',
            'low': 'red',
            'high': 'red',
            'unknown': 'gray',
        }.get(self.status, 'gray')


class AILicense(models.Model):
    """Licencia global de IA para toda la instalación (singleton)."""

    api_key = models.CharField(max_length=255, verbose_name=_('AI API key'))
    plan = models.CharField(max_length=50, default='premium', verbose_name=_('Plan'))
    activated_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Activated at'))
    activated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name='ai_licenses', verbose_name=_('Activated by')
    )

    class Meta:
        verbose_name = _('AI license')
        verbose_name_plural = _('AI licenses')

    def __str__(self):
        return f'Licencia {self.plan} ({self.activated_at:%Y-%m-%d})'

    @classmethod
    def get_active(cls):
        """Devuelve la licencia activa o None."""
        return cls.objects.order_by('-activated_at').first()
