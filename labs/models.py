"""Modelos de datos de LabLocal."""
import uuid
from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver




class UserProfile(models.Model):
    """Perfil extendido del usuario con datos médicos básicos."""
    def avatar_upload_path(_instance, filename):
        ext = filename.split('.')[-1]
        return f'avatars/{uuid.uuid4()}.{ext}'

    SEXO_CHOICES = [('M', 'Masculino'), ('F', 'Femenino')]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    avatar = models.ImageField(
        upload_to=avatar_upload_path,
        null=True, blank=True, verbose_name='Foto de perfil'
    )
    birth_date = models.DateField(null=True, blank=True, verbose_name='Fecha de nacimiento')
    biological_sex = models.CharField(
        max_length=1, choices=SEXO_CHOICES, blank=True, verbose_name='Sexo biológico'
    )
    notes = models.TextField(blank=True, verbose_name='Notas')

    class Meta:
        verbose_name = 'Perfil de usuario'
        verbose_name_plural = 'Perfiles de usuario'

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
        ('HEMATOLOGIA', 'Hematología'),
        ('BIOQUIMICA', 'Bioquímica'),
        ('LIPIDOS', 'Lípidos'),
        ('TIROIDES', 'Tiroides'),
        ('HIERRO', 'Hierro'),
        ('INFLAMACION', 'Inflamación'),
        ('ORINA', 'Orina'),
        ('VITAMINAS', 'Vitaminas'),
        ('OTRO', 'Otro'),
    ]

    name = models.CharField(max_length=200, verbose_name='Nombre')
    short_name = models.CharField(max_length=50, verbose_name='Nombre corto')
    loinc_code = models.CharField(max_length=20, blank=True, verbose_name='Código LOINC')
    category = models.CharField(
        max_length=20, choices=CATEGORIA_CHOICES, default='OTRO', verbose_name='Categoría'
    )
    unit = models.CharField(max_length=50, verbose_name='Unidad')
    description = models.TextField(blank=True, verbose_name='Descripción')
    ref_min_male = models.DecimalField(
        max_digits=10, decimal_places=3, null=True, blank=True,
        verbose_name='Rango mínimo (hombre)'
    )
    ref_max_male = models.DecimalField(
        max_digits=10, decimal_places=3, null=True, blank=True,
        verbose_name='Rango máximo (hombre)'
    )
    ref_min_female = models.DecimalField(
        max_digits=10, decimal_places=3, null=True, blank=True,
        verbose_name='Rango mínimo (mujer)'
    )
    ref_max_female = models.DecimalField(
        max_digits=10, decimal_places=3, null=True, blank=True,
        verbose_name='Rango máximo (mujer)'
    )
    low_is_bad = models.BooleanField(
        default=True, verbose_name='Valor bajo es malo'
    )
    order = models.PositiveIntegerField(default=0, verbose_name='Orden')

    class Meta:
        verbose_name = 'Biomarcador'
        verbose_name_plural = 'Biomarcadores'
        ordering = ['category', 'order', 'name']

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
        related_name='%(class)s_reports', verbose_name='Usuario'
    )
    name = models.CharField(max_length=200, verbose_name='Nombre')
    date = models.DateField(verbose_name='Fecha')
    notes = models.TextField(blank=True, verbose_name='Notas')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creado el')

    class Meta:
        abstract = True
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f'{self.name} — {self.date}'


class AnalysisReport(BaseReport):
    """Analítica o reconocimiento médico completo."""

    lab_name = models.CharField(max_length=200, blank=True, verbose_name='Laboratorio')
    phenoage_years = models.DecimalField(
        max_digits=5, decimal_places=1, null=True, blank=True,
        verbose_name='Edad biológica (PhenoAge)'
    )
    phenoage_delta_years = models.DecimalField(
        max_digits=5, decimal_places=1, null=True, blank=True,
        verbose_name='Diferencia edad biológica-cronológica'
    )
    phenoage_missing = models.TextField(
        blank=True, default='',
        verbose_name='Marcadores faltantes para PhenoAge'
    )

    class Meta(BaseReport.Meta):
        verbose_name = 'Analítica'
        verbose_name_plural = 'Analíticas'

    def get_alerts(self):
        """Devuelve los resultados fuera de rango normal."""
        return [r for r in self.results.select_related('biomarker') if r.status in ('low', 'high')]

    def get_borderlines(self):
        """Devuelve los resultados en límite."""
        return [r for r in self.results.select_related('biomarker') if r.status == 'borderline']


class BodyCompositionReport(BaseReport):
    """Registro de composición corporal (báscula inteligente o medición manual)."""

    weight = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name='Peso (kg)'
    )
    height = models.DecimalField(
        max_digits=5, decimal_places=1, verbose_name='Altura (cm)'
    )
    body_fat_pct = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        verbose_name='Grasa corporal (%)'
    )
    visceral_fat = models.DecimalField(
        max_digits=5, decimal_places=1, null=True, blank=True,
        verbose_name='Grasa visceral (nivel)'
    )
    muscle_mass = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        verbose_name='Masa muscular (kg)'
    )
    water_pct = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        verbose_name='Agua (%)'
    )
    protein_pct = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        verbose_name='Proteína (%)'
    )
    bone_mass = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        verbose_name='Masa ósea (kg)'
    )

    class Meta(BaseReport.Meta):
        verbose_name = 'Composición corporal'
        verbose_name_plural = 'Composiciones corporales'

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
            return ('Sin datos', 'unknown')
        if bmi < 18.5:
            return ('Bajo peso', 'low')
        if bmi < 25.0:
            return ('Normal', 'normal')
        if bmi < 30.0:
            return ('Sobrepeso', 'borderline')
        return ('Obesidad', 'high')



class ECGReport(BaseReport):
    """Registro de electrocardiograma (ECG/EKG)."""
    def ecg_image_upload_path(_instance, filename):
        ext = filename.split('.')[-1]
        return f'ecg/{uuid.uuid4()}.{ext}'

    image = models.ImageField(
        upload_to=ecg_image_upload_path,
        verbose_name='Imagen de ECG'
    )
    heart_rate = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="Frecuencia cardíaca (bpm)"
    )

    class Meta(BaseReport.Meta):
        verbose_name = 'Electrocardiograma'
        verbose_name_plural = 'Electrocardiogramas'

    def __str__(self):
        return f'ECG — {self.name} ({self.date})'


class BiomarkerResult(models.Model):
    """Valor de un biomarcador en una analítica concreta."""

    report = models.ForeignKey(
        AnalysisReport, on_delete=models.CASCADE, related_name='results', verbose_name='Analítica'
    )
    biomarker = models.ForeignKey(
        Biomarker, on_delete=models.PROTECT, related_name='results', verbose_name='Biomarcador'
    )
    value = models.DecimalField(max_digits=12, decimal_places=4, verbose_name='Valor')
    notes = models.TextField(blank=True, verbose_name='Notas')

    class Meta:
        verbose_name = 'Resultado'
        verbose_name_plural = 'Resultados'
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
            'normal': 'Normal',
            'borderline': 'Límite',
            'low': 'Bajo',
            'high': 'Alto',
            'unknown': 'Sin rango',
        }.get(self.status, 'Desconocido')

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
