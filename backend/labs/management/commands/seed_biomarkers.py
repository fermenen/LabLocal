"""Comando para cargar el catálogo de biomarcadores en la base de datos.

Solo almacena datos científicos puros (unidades, rangos de referencia, etc.).
Los nombres y descripciones viven en labs/biomarker_i18n.py.
"""
from django.core.management.base import BaseCommand

from labs.models import Biomarker

BIOMARKERS = [
    # ── HEMATOLOGÍA ────────────────────────────────────────────────────────────
    {
        'loinc_code': '6690-2',
        'category': 'HEMATOLOGIA', 'unit': '10³/μL', 'order': 1,
        'ref_min_male': 4.5, 'ref_max_male': 11.0,
        'ref_min_female': 4.5, 'ref_max_female': 11.0,
        'low_is_bad': True,
    },
    {
        'loinc_code': '789-8',
        'category': 'HEMATOLOGIA', 'unit': '10⁶/μL', 'order': 2,
        'ref_min_male': 4.5, 'ref_max_male': 5.9,
        'ref_min_female': 3.8, 'ref_max_female': 5.2,
        'low_is_bad': True,
    },
    {
        'loinc_code': '718-7',
        'category': 'HEMATOLOGIA', 'unit': 'g/dL', 'order': 3,
        'ref_min_male': 13.5, 'ref_max_male': 17.5,
        'ref_min_female': 12.0, 'ref_max_female': 16.0,
        'low_is_bad': True,
    },
    {
        'loinc_code': '4544-3',
        'category': 'HEMATOLOGIA', 'unit': '%', 'order': 4,
        'ref_min_male': 41.0, 'ref_max_male': 53.0,
        'ref_min_female': 36.0, 'ref_max_female': 46.0,
        'low_is_bad': True,
    },
    {
        'loinc_code': '787-2',
        'category': 'HEMATOLOGIA', 'unit': 'fL', 'order': 5,
        'ref_min_male': 80.0, 'ref_max_male': 100.0,
        'ref_min_female': 80.0, 'ref_max_female': 100.0,
        'low_is_bad': False,
    },
    {
        'loinc_code': '785-6',
        'category': 'HEMATOLOGIA', 'unit': 'pg', 'order': 6,
        'ref_min_male': 26.0, 'ref_max_male': 34.0,
        'ref_min_female': 26.0, 'ref_max_female': 34.0,
        'low_is_bad': False,
    },
    {
        'loinc_code': '786-4',
        'category': 'HEMATOLOGIA', 'unit': 'g/dL', 'order': 7,
        'ref_min_male': 32.0, 'ref_max_male': 36.0,
        'ref_min_female': 32.0, 'ref_max_female': 36.0,
        'low_is_bad': False,
    },
    {
        'loinc_code': '777-3',
        'category': 'HEMATOLOGIA', 'unit': '10³/μL', 'order': 8,
        'ref_min_male': 150.0, 'ref_max_male': 400.0,
        'ref_min_female': 150.0, 'ref_max_female': 400.0,
        'low_is_bad': True,
    },
    {
        'loinc_code': '751-8',
        'category': 'HEMATOLOGIA', 'unit': '10³/μL', 'order': 9,
        'ref_min_male': 1.8, 'ref_max_male': 7.7,
        'ref_min_female': 1.8, 'ref_max_female': 7.7,
        'low_is_bad': True,
    },
    {
        'loinc_code': '731-0',
        'category': 'HEMATOLOGIA', 'unit': '10³/μL', 'order': 10,
        'ref_min_male': 1.0, 'ref_max_male': 4.8,
        'ref_min_female': 1.0, 'ref_max_female': 4.8,
        'low_is_bad': True,
    },
    {
        'loinc_code': '742-7',
        'category': 'HEMATOLOGIA', 'unit': '10³/μL', 'order': 11,
        'ref_min_male': 0.1, 'ref_max_male': 1.2,
        'ref_min_female': 0.1, 'ref_max_female': 1.2,
        'low_is_bad': False,
    },
    {
        'loinc_code': '711-2',
        'category': 'HEMATOLOGIA', 'unit': '10³/μL', 'order': 12,
        'ref_min_male': 0.0, 'ref_max_male': 0.5,
        'ref_min_female': 0.0, 'ref_max_female': 0.5,
        'low_is_bad': False,
    },
    {
        'loinc_code': '704-7',
        'category': 'HEMATOLOGIA', 'unit': '10³/μL', 'order': 13,
        'ref_min_male': 0.0, 'ref_max_male': 0.1,
        'ref_min_female': 0.0, 'ref_max_female': 0.1,
        'low_is_bad': False,
    },
    {
        'loinc_code': '788-0',
        'category': 'HEMATOLOGIA', 'unit': '%', 'order': 14,
        'ref_min_male': 11.5, 'ref_max_male': 14.5,
        'ref_min_female': 11.5, 'ref_max_female': 14.5,
        'low_is_bad': False,
    },

    # ── BIOQUÍMICA ─────────────────────────────────────────────────────────────
    {
        'loinc_code': '2345-7',
        'category': 'BIOQUIMICA', 'unit': 'mg/dL', 'order': 1,
        'ref_min_male': 70.0, 'ref_max_male': 100.0,
        'ref_min_female': 70.0, 'ref_max_female': 100.0,
        'low_is_bad': False,
    },
    {
        'loinc_code': '4548-4',
        'category': 'BIOQUIMICA', 'unit': '%', 'order': 2,
        'ref_min_male': 4.0, 'ref_max_male': 6.0,
        'ref_min_female': 4.0, 'ref_max_female': 6.0,
        'low_is_bad': False,
    },
    {
        'loinc_code': '3091-6',
        'category': 'BIOQUIMICA', 'unit': 'mg/dL', 'order': 3,
        'ref_min_male': 15.0, 'ref_max_male': 45.0,
        'ref_min_female': 15.0, 'ref_max_female': 45.0,
        'low_is_bad': False,
    },
    {
        'loinc_code': '2160-0',
        'category': 'BIOQUIMICA', 'unit': 'mg/dL', 'order': 4,
        'ref_min_male': 0.7, 'ref_max_male': 1.2,
        'ref_min_female': 0.5, 'ref_max_female': 1.0,
        'low_is_bad': False,
    },
    {
        'loinc_code': '3084-1',
        'category': 'BIOQUIMICA', 'unit': 'mg/dL', 'order': 5,
        'ref_min_male': 3.4, 'ref_max_male': 7.2,
        'ref_min_female': 2.4, 'ref_max_female': 5.7,
        'low_is_bad': False,
    },
    {
        'loinc_code': '1975-2',
        'category': 'BIOQUIMICA', 'unit': 'mg/dL', 'order': 6,
        'ref_min_male': 0.2, 'ref_max_male': 1.2,
        'ref_min_female': 0.2, 'ref_max_female': 1.2,
        'low_is_bad': False,
    },
    {
        'loinc_code': '2885-2',
        'category': 'BIOQUIMICA', 'unit': 'g/dL', 'order': 7,
        'ref_min_male': 6.4, 'ref_max_male': 8.2,
        'ref_min_female': 6.4, 'ref_max_female': 8.2,
        'low_is_bad': True,
    },
    {
        'loinc_code': '1751-7',
        'category': 'BIOQUIMICA', 'unit': 'g/dL', 'order': 8,
        'ref_min_male': 3.5, 'ref_max_male': 5.0,
        'ref_min_female': 3.5, 'ref_max_female': 5.0,
        'low_is_bad': True,
    },
    {
        'loinc_code': '1920-8',
        'category': 'BIOQUIMICA', 'unit': 'U/L', 'order': 9,
        'ref_min_male': 10.0, 'ref_max_male': 40.0,
        'ref_min_female': 10.0, 'ref_max_female': 35.0,
        'low_is_bad': False,
    },
    {
        'loinc_code': '1742-6',
        'category': 'BIOQUIMICA', 'unit': 'U/L', 'order': 10,
        'ref_min_male': 10.0, 'ref_max_male': 45.0,
        'ref_min_female': 10.0, 'ref_max_female': 35.0,
        'low_is_bad': False,
    },
    {
        'loinc_code': '2324-2',
        'category': 'BIOQUIMICA', 'unit': 'U/L', 'order': 11,
        'ref_min_male': 9.0, 'ref_max_male': 48.0,
        'ref_min_female': 9.0, 'ref_max_female': 32.0,
        'low_is_bad': False,
    },
    {
        'loinc_code': '6768-6',
        'category': 'BIOQUIMICA', 'unit': 'U/L', 'order': 12,
        'ref_min_male': 40.0, 'ref_max_male': 130.0,
        'ref_min_female': 40.0, 'ref_max_female': 130.0,
        'low_is_bad': False,
    },

    # ── LÍPIDOS ────────────────────────────────────────────────────────────────
    {
        'loinc_code': '2093-3',
        'category': 'LIPIDOS', 'unit': 'mg/dL', 'order': 1,
        'ref_min_male': None, 'ref_max_male': 200.0,
        'ref_min_female': None, 'ref_max_female': 200.0,
        'low_is_bad': False,
    },
    {
        'loinc_code': '2085-9',
        'category': 'LIPIDOS', 'unit': 'mg/dL', 'order': 2,
        'ref_min_male': 40.0, 'ref_max_male': None,
        'ref_min_female': 50.0, 'ref_max_female': None,
        'low_is_bad': True,
    },
    {
        'loinc_code': '2089-1',
        'category': 'LIPIDOS', 'unit': 'mg/dL', 'order': 3,
        'ref_min_male': None, 'ref_max_male': 130.0,
        'ref_min_female': None, 'ref_max_female': 130.0,
        'low_is_bad': False,
    },
    {
        'loinc_code': '2571-8',
        'category': 'LIPIDOS', 'unit': 'mg/dL', 'order': 4,
        'ref_min_male': None, 'ref_max_male': 150.0,
        'ref_min_female': None, 'ref_max_female': 150.0,
        'low_is_bad': False,
    },
    {
        'loinc_code': 'ATHEROGENIC_INDEX',
        'category': 'LIPIDOS', 'unit': 'ratio', 'order': 5,
        'ref_min_male': None, 'ref_max_male': 5.0,
        'ref_min_female': None, 'ref_max_female': 4.5,
        'low_is_bad': False,
    },

    # ── TIROIDES ───────────────────────────────────────────────────────────────
    {
        'loinc_code': '3016-3',
        'category': 'TIROIDES', 'unit': 'mUI/L', 'order': 1,
        'ref_min_male': 0.4, 'ref_max_male': 4.0,
        'ref_min_female': 0.4, 'ref_max_female': 4.0,
        'low_is_bad': False,
    },
    {
        'loinc_code': '3024-7',
        'category': 'TIROIDES', 'unit': 'ng/dL', 'order': 2,
        'ref_min_male': 0.8, 'ref_max_male': 1.8,
        'ref_min_female': 0.8, 'ref_max_female': 1.8,
        'low_is_bad': True,
    },

    # ── HIERRO ─────────────────────────────────────────────────────────────────
    {
        'loinc_code': '2498-4',
        'category': 'HIERRO', 'unit': 'μg/dL', 'order': 1,
        'ref_min_male': 65.0, 'ref_max_male': 175.0,
        'ref_min_female': 50.0, 'ref_max_female': 170.0,
        'low_is_bad': True,
    },
    {
        'loinc_code': '2276-4',
        'category': 'HIERRO', 'unit': 'ng/mL', 'order': 2,
        'ref_min_male': 30.0, 'ref_max_male': 300.0,
        'ref_min_female': 12.0, 'ref_max_female': 150.0,
        'low_is_bad': True,
    },
    {
        'loinc_code': '3034-6',
        'category': 'HIERRO', 'unit': 'mg/dL', 'order': 3,
        'ref_min_male': 200.0, 'ref_max_male': 360.0,
        'ref_min_female': 200.0, 'ref_max_female': 360.0,
        'low_is_bad': True,
    },
    {
        'loinc_code': '2502-3',
        'category': 'HIERRO', 'unit': '%', 'order': 4,
        'ref_min_male': 20.0, 'ref_max_male': 50.0,
        'ref_min_female': 20.0, 'ref_max_female': 50.0,
        'low_is_bad': True,
    },
    {
        'loinc_code': '2500-7',
        'category': 'HIERRO', 'unit': 'μg/dL', 'order': 5,
        'ref_min_male': 250.0, 'ref_max_male': 370.0,
        'ref_min_female': 250.0, 'ref_max_female': 370.0,
        'low_is_bad': False,
    },

    # ── INFLAMACIÓN ────────────────────────────────────────────────────────────
    {
        'loinc_code': '1988-5',
        'category': 'INFLAMACION', 'unit': 'mg/L', 'order': 1,
        'ref_min_male': None, 'ref_max_male': 5.0,
        'ref_min_female': None, 'ref_max_female': 5.0,
        'low_is_bad': False,
    },
    {
        'loinc_code': '4537-7',
        'category': 'INFLAMACION', 'unit': 'mm/h', 'order': 2,
        'ref_min_male': None, 'ref_max_male': 15.0,
        'ref_min_female': None, 'ref_max_female': 20.0,
        'low_is_bad': False,
    },
    {
        'loinc_code': '3255-7',
        'category': 'INFLAMACION', 'unit': 'mg/dL', 'order': 3,
        'ref_min_male': 200.0, 'ref_max_male': 400.0,
        'ref_min_female': 200.0, 'ref_max_female': 400.0,
        'low_is_bad': True,
    },

    # ── ORINA ──────────────────────────────────────────────────────────────────
    {
        'loinc_code': '2756-5',
        'category': 'ORINA', 'unit': '', 'order': 1,
        'ref_min_male': 5.0, 'ref_max_male': 8.0,
        'ref_min_female': 5.0, 'ref_max_female': 8.0,
        'low_is_bad': False,
    },
    {
        'loinc_code': '5811-5',
        'category': 'ORINA', 'unit': '', 'order': 2,
        'ref_min_male': 1.005, 'ref_max_male': 1.030,
        'ref_min_female': 1.005, 'ref_max_female': 1.030,
        'low_is_bad': False,
    },
    {
        'loinc_code': '2349-9',
        'category': 'ORINA', 'unit': 'mg/dL', 'order': 3,
        'ref_min_male': None, 'ref_max_male': 15.0,
        'ref_min_female': None, 'ref_max_female': 15.0,
        'low_is_bad': False,
    },
    {
        'loinc_code': '2888-6',
        'category': 'ORINA', 'unit': 'mg/dL', 'order': 4,
        'ref_min_male': None, 'ref_max_male': 14.0,
        'ref_min_female': None, 'ref_max_female': 14.0,
        'low_is_bad': False,
    },
    {
        'loinc_code': '5821-4',
        'category': 'ORINA', 'unit': '/campo', 'order': 5,
        'ref_min_male': None, 'ref_max_male': 5.0,
        'ref_min_female': None, 'ref_max_female': 5.0,
        'low_is_bad': False,
    },
    {
        'loinc_code': '13945-1',
        'category': 'ORINA', 'unit': '/campo', 'order': 6,
        'ref_min_male': None, 'ref_max_male': 2.0,
        'ref_min_female': None, 'ref_max_female': 3.0,
        'low_is_bad': False,
    },
    {
        'loinc_code': '2514-8',
        'category': 'ORINA', 'unit': 'mg/dL', 'order': 7,
        'ref_min_male': None, 'ref_max_male': 0.0,
        'ref_min_female': None, 'ref_max_female': 0.0,
        'low_is_bad': False,
    },

    # ── VITAMINAS ──────────────────────────────────────────────────────────────
    {
        'loinc_code': '1989-3',
        'category': 'VITAMINAS', 'unit': 'ng/mL', 'order': 1,
        'ref_min_male': 30.0, 'ref_max_male': 100.0,
        'ref_min_female': 30.0, 'ref_max_female': 100.0,
        'low_is_bad': True,
    },
    {
        'loinc_code': '2132-9',
        'category': 'VITAMINAS', 'unit': 'pg/mL', 'order': 2,
        'ref_min_male': 200.0, 'ref_max_male': 900.0,
        'ref_min_female': 200.0, 'ref_max_female': 900.0,
        'low_is_bad': True,
    },
    {
        'loinc_code': '2284-8',
        'category': 'VITAMINAS', 'unit': 'ng/mL', 'order': 3,
        'ref_min_male': 3.0, 'ref_max_male': 17.0,
        'ref_min_female': 3.0, 'ref_max_female': 17.0,
        'low_is_bad': True,
    },

    # ── OTRO ───────────────────────────────────────────────────────────────────
    {
        'loinc_code': '2857-1',
        'category': 'OTRO', 'unit': 'ng/mL', 'order': 1,
        'ref_min_male': None, 'ref_max_male': 4.0,
        'ref_min_female': None, 'ref_max_female': None,
        'low_is_bad': False,
    },
    {
        'loinc_code': '17861-6',
        'category': 'OTRO', 'unit': 'mg/dL', 'order': 2,
        'ref_min_male': 8.5, 'ref_max_male': 10.5,
        'ref_min_female': 8.5, 'ref_max_female': 10.5,
        'low_is_bad': True,
    },
    {
        'loinc_code': '2777-1',
        'category': 'OTRO', 'unit': 'mg/dL', 'order': 3,
        'ref_min_male': 2.5, 'ref_max_male': 4.5,
        'ref_min_female': 2.5, 'ref_max_female': 4.5,
        'low_is_bad': True,
    },
    {
        'loinc_code': '2951-2',
        'category': 'OTRO', 'unit': 'mEq/L', 'order': 4,
        'ref_min_male': 136.0, 'ref_max_male': 145.0,
        'ref_min_female': 136.0, 'ref_max_female': 145.0,
        'low_is_bad': True,
    },
    {
        'loinc_code': '2823-3',
        'category': 'OTRO', 'unit': 'mEq/L', 'order': 5,
        'ref_min_male': 3.5, 'ref_max_male': 5.1,
        'ref_min_female': 3.5, 'ref_max_female': 5.1,
        'low_is_bad': True,
    },
    {
        'loinc_code': '2075-0',
        'category': 'OTRO', 'unit': 'mEq/L', 'order': 6,
        'ref_min_male': 98.0, 'ref_max_male': 107.0,
        'ref_min_female': 98.0, 'ref_max_female': 107.0,
        'low_is_bad': True,
    },
]


class Command(BaseCommand):
    """Carga el catálogo de biomarcadores en la base de datos."""

    help = 'Carga o actualiza el catálogo de biomarcadores (idempotente)'

    def handle(self, *args, **options):
        creados = 0
        actualizados = 0
        for data in BIOMARKERS:
            obj, created = Biomarker.objects.update_or_create(
                loinc_code=data['loinc_code'],
                defaults={
                    'category': data['category'],
                    'unit': data['unit'],
                    'ref_min_male': data.get('ref_min_male'),
                    'ref_max_male': data.get('ref_max_male'),
                    'ref_min_female': data.get('ref_min_female'),
                    'ref_max_female': data.get('ref_max_female'),
                    'low_is_bad': data.get('low_is_bad', True),
                    'order': data.get('order', 0),
                },
            )
            if created:
                creados += 1
            else:
                actualizados += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Biomarcadores cargados: {creados} nuevos, {actualizados} actualizados.'
            )
        )
