"""Comando para poblar datos de demostración en el usuario admin."""
import datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from labs.models import AnalysisReport, Biomarker, BiomarkerResult
from labs.phenoage import update_report_phenoage


# (short_name, valor_report1, valor_report2)
# report1 = hace ~1 año — valores saludables  → PhenoAge < edad cronológica
# report2 = reciente    — valores alterados   → PhenoAge > edad cronológica
#
# Biomarcadores para PhenoAge (Levine 2018): ALB, CREA, GLU, PCR, VCM, RDW, FA, WBC, LYMPH
DEMO_VALUES = [
    # ── HEMATOLOGÍA ────────────────────────────────────────────────────────────
    # Leucocitos        normal 4.5–11.0 10³/μL   [PhenoAge: WBC]
    ('WBC',    6.5,   11.5),   # normal → ALTO
    # Eritrocitos       normal 4.5–5.9 10⁶/μL
    ('RBC',    5.1,    4.6),   # normal → normal
    # Hemoglobina       normal 13.5–17.5 g/dL
    ('HGB',   15.2,   11.8),   # normal → BAJO
    # Hematocrito       normal 41–53 %
    ('HCT',   45.5,   38.0),   # normal → límite bajo
    # VCM               normal 80–100 fL          [PhenoAge: MCV]
    ('VCM',   88.0,   93.0),   # normal → normal-alto
    # RDW               normal 11.5–14.5 %        [PhenoAge: RDW]
    ('RDW',   12.0,   14.8),   # normal → límite ALTO
    # Plaquetas         normal 150–400 10³/μL
    ('PLT',  215.0,  125.0),   # normal → BAJO
    # Neutrófilos       normal 1.8–7.7 10³/μL
    ('NEUT',   3.5,    8.8),   # normal → ALTO
    # Linfocitos        normal 1.0–4.8 10³/μL     [PhenoAge: LYMPH/WBC × 100]
    ('LYMPH',  2.5,    1.1),   # 38 % → 9.6 %   (linfopenia relativa)
    # ── BIOQUÍMICA ─────────────────────────────────────────────────────────────
    # Glucosa           normal 70–100 mg/dL        [PhenoAge: GLU]
    ('GLU',   88.0,  112.0),   # normal → prediabetes
    # HbA1c             normal 4.0–6.0 %
    ('HbA1c',  5.1,    6.4),   # normal → límite alto
    # Creatinina        normal 0.7–1.2 mg/dL       [PhenoAge: CREA]
    ('CREA',   0.90,   1.48),  # normal → ALTO
    # Albúmina          normal 3.5–5.0 g/dL        [PhenoAge: ALB]
    ('ALB',    4.8,    4.0),   # alto-normal → normal-bajo
    # Fosfatasa Alc.    normal 40–130 U/L           [PhenoAge: ALP]
    ('FA',    68.0,  128.0),   # normal → límite
    # AST               normal 10–40 U/L
    ('AST',   20.0,   52.0),   # normal → ALTO
    # ALT               normal 10–45 U/L
    ('ALT',   25.0,   88.0),   # normal → ALTO
    # GGT               normal 9–48 U/L
    ('GGT',   28.0,   95.0),   # normal → ALTO
    # ── LÍPIDOS ────────────────────────────────────────────────────────────────
    # Colesterol total  normal <200 mg/dL
    ('COL',  175.0,  232.0),   # normal → ALTO
    # HDL               normal >40 mg/dL
    ('HDL',   58.0,   32.0),   # normal → BAJO
    # LDL               normal <130 mg/dL
    ('LDL',   95.0,  165.0),   # normal → ALTO
    # Triglicéridos     normal <150 mg/dL
    ('TG',   105.0,  290.0),   # normal → ALTO
    # ── TIROIDES ───────────────────────────────────────────────────────────────
    ('TSH',    1.9,    6.5),   # normal → ALTO (hipotiroidismo subclínico)
    # ── HIERRO ─────────────────────────────────────────────────────────────────
    ('FERR',  155.0,   16.0),  # normal → BAJA
    ('FE',    105.0,   38.0),  # normal → BAJO
    # ── INFLAMACIÓN ────────────────────────────────────────────────────────────
    # PCR               normal <5 mg/L              [PhenoAge: CRP]
    ('PCR',    0.5,   12.0),   # muy baja → ALTA
    # ── VITAMINAS ──────────────────────────────────────────────────────────────
    ('VIT-D',  45.0,   12.0),  # normal → BAJO
    ('B12',   420.0,  145.0),  # normal → BAJO
]

REPORT_1 = {
    'name': 'Reconocimiento laboral 2025',
    'date': datetime.date(2025, 3, 15),
    'lab_name': 'Laboratorio Clínico Central',
    'notes': 'Analítica anual de empresa. Resultados excelentes.',
}

REPORT_2 = {
    'name': 'Analítica de control',
    'date': datetime.date(2026, 2, 10),
    'lab_name': 'Clínica San Marcos',
    'notes': 'Revisión por cansancio persistente y mareos. Varios valores alterados.',
}


class Command(BaseCommand):
    help = 'Carga datos de demostración (analíticas con valores buenos y malos) para el usuario admin.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Elimina las analíticas de demo existentes antes de crearlas de nuevo.',
        )

    def handle(self, *args, **options):
        try:
            user = User.objects.get(username='admin')
        except User.DoesNotExist:
            self.stderr.write(self.style.ERROR(
                'No existe el usuario "admin". Ejecútalo tras crear el superusuario.'
            ))
            return

        # Asegurar perfil con datos médicos básicos
        profile = user.userprofile
        if not profile.biological_sex:
            profile.biological_sex = 'M'
        if not profile.birth_date:
            profile.birth_date = datetime.date(1985, 6, 20)
        profile.save()

        # Construir índice de biomarcadores por short_name
        biomarkers = {b.short_name: b for b in Biomarker.objects.all()}
        if not biomarkers:
            self.stderr.write(self.style.ERROR(
                'No hay biomarcadores. Ejecuta primero: python manage.py seed_biomarkers'
            ))
            return

        if options['reset']:
            deleted, _ = AnalysisReport.objects.filter(
                user=user,
                name__in=[REPORT_1['name'], REPORT_2['name']],
            ).delete()
            self.stdout.write(f'  Eliminadas {deleted} analítica(s) existentes.')

        creados = 0
        omitidos = 0

        for report_data, valor_idx in [(REPORT_1, 1), (REPORT_2, 2)]:
            report, created = AnalysisReport.objects.get_or_create(
                user=user,
                name=report_data['name'],
                defaults={
                    'date': report_data['date'],
                    'lab_name': report_data['lab_name'],
                    'notes': report_data['notes'],
                },
            )
            if not created:
                self.stdout.write(f'  Analítica ya existe, omitiendo: {report.name}')
                omitidos += 1
                continue

            for short_name, val1, val2 in DEMO_VALUES:
                biomarker = biomarkers.get(short_name)
                if biomarker is None:
                    self.stderr.write(f'    ⚠ Biomarcador no encontrado: {short_name}')
                    continue
                value = val1 if valor_idx == 1 else val2
                BiomarkerResult.objects.create(
                    report=report,
                    biomarker=biomarker,
                    value=value,
                )

            update_report_phenoage(report)

            creados += 1
            self.stdout.write(self.style.SUCCESS(f'  ✓ {report.name} ({report.date})'))

        self.stdout.write(self.style.SUCCESS(
            f'\nListo. {creados} analíticas creadas, {omitidos} omitidas (ya existían).'
        ))
