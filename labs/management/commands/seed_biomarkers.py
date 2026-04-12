"""Comando para cargar el catálogo de biomarcadores en la base de datos."""
from django.core.management.base import BaseCommand

from labs.models import Biomarker

BIOMARKERS = [
    # ── HEMATOLOGÍA ────────────────────────────────────────────────────────────
    {
        'name': 'Leucocitos', 'short_name': 'WBC', 'loinc_code': '6690-2',
        'category': 'HEMATOLOGIA', 'unit': '10³/μL', 'order': 1,
        'ref_min_male': 4.5, 'ref_max_male': 11.0,
        'ref_min_female': 4.5, 'ref_max_female': 11.0,
        'low_is_bad': True,
        'description': (
            'Glóbulos blancos. Son las células del sistema inmune. '
            'Valores altos pueden indicar infección o inflamación; '
            'valores bajos pueden indicar inmunosupresión.'
        ),
    },
    {
        'name': 'Eritrocitos', 'short_name': 'RBC', 'loinc_code': '789-8',
        'category': 'HEMATOLOGIA', 'unit': '10⁶/μL', 'order': 2,
        'ref_min_male': 4.5, 'ref_max_male': 5.9,
        'ref_min_female': 3.8, 'ref_max_female': 5.2,
        'low_is_bad': True,
        'description': (
            'Glóbulos rojos. Transportan oxígeno desde los pulmones al resto del cuerpo. '
            'Su recuento bajo puede indicar anemia.'
        ),
    },
    {
        'name': 'Hemoglobina', 'short_name': 'HGB', 'loinc_code': '718-7',
        'category': 'HEMATOLOGIA', 'unit': 'g/dL', 'order': 3,
        'ref_min_male': 13.5, 'ref_max_male': 17.5,
        'ref_min_female': 12.0, 'ref_max_female': 16.0,
        'low_is_bad': True,
        'description': (
            'Proteína dentro de los glóbulos rojos que transporta el oxígeno. '
            'Es el principal indicador de anemia.'
        ),
    },
    {
        'name': 'Hematocrito', 'short_name': 'HCT', 'loinc_code': '4544-3',
        'category': 'HEMATOLOGIA', 'unit': '%', 'order': 4,
        'ref_min_male': 41.0, 'ref_max_male': 53.0,
        'ref_min_female': 36.0, 'ref_max_female': 46.0,
        'low_is_bad': True,
        'description': (
            'Porcentaje del volumen sanguíneo ocupado por glóbulos rojos. '
            'Complementa a la hemoglobina para valorar la anemia.'
        ),
    },
    {
        'name': 'Volumen Corpuscular Medio', 'short_name': 'VCM', 'loinc_code': '787-2',
        'category': 'HEMATOLOGIA', 'unit': 'fL', 'order': 5,
        'ref_min_male': 80.0, 'ref_max_male': 100.0,
        'ref_min_female': 80.0, 'ref_max_female': 100.0,
        'low_is_bad': False,
        'description': (
            'Tamaño medio de los glóbulos rojos. '
            'Valores bajos (microcitosis) se asocian con deficiencia de hierro; '
            'valores altos (macrocitosis) con deficiencia de B12 o folato.'
        ),
    },
    {
        'name': 'Hemoglobina Corpuscular Media', 'short_name': 'HCM', 'loinc_code': '785-6',
        'category': 'HEMATOLOGIA', 'unit': 'pg', 'order': 6,
        'ref_min_male': 26.0, 'ref_max_male': 34.0,
        'ref_min_female': 26.0, 'ref_max_female': 34.0,
        'low_is_bad': False,
        'description': 'Cantidad media de hemoglobina por glóbulo rojo.',
    },
    {
        'name': 'Concentración de Hemoglobina Corpuscular Media', 'short_name': 'CHCM',
        'loinc_code': '786-4', 'category': 'HEMATOLOGIA', 'unit': 'g/dL', 'order': 7,
        'ref_min_male': 32.0, 'ref_max_male': 36.0,
        'ref_min_female': 32.0, 'ref_max_female': 36.0,
        'low_is_bad': False,
        'description': 'Concentración de hemoglobina en relación al volumen del glóbulo rojo.',
    },
    {
        'name': 'Plaquetas', 'short_name': 'PLT', 'loinc_code': '777-3',
        'category': 'HEMATOLOGIA', 'unit': '10³/μL', 'order': 8,
        'ref_min_male': 150.0, 'ref_max_male': 400.0,
        'ref_min_female': 150.0, 'ref_max_female': 400.0,
        'low_is_bad': True,
        'description': (
            'Fragmentos celulares implicados en la coagulación. '
            'Valores bajos aumentan el riesgo de hemorragia; '
            'valores altos pueden asociarse a trombosis.'
        ),
    },
    {
        'name': 'Neutrófilos', 'short_name': 'NEUT', 'loinc_code': '751-8',
        'category': 'HEMATOLOGIA', 'unit': '10³/μL', 'order': 9,
        'ref_min_male': 1.8, 'ref_max_male': 7.7,
        'ref_min_female': 1.8, 'ref_max_female': 7.7,
        'low_is_bad': True,
        'description': (
            'Tipo de leucocito, primera línea de defensa contra infecciones bacterianas. '
            'Su aumento (neutrofilia) suele indicar infección aguda.'
        ),
    },
    {
        'name': 'Linfocitos', 'short_name': 'LYMPH', 'loinc_code': '731-0',
        'category': 'HEMATOLOGIA', 'unit': '10³/μL', 'order': 10,
        'ref_min_male': 1.0, 'ref_max_male': 4.8,
        'ref_min_female': 1.0, 'ref_max_female': 4.8,
        'low_is_bad': True,
        'description': (
            'Leucocitos clave en la respuesta inmune adaptativa. '
            'Muy elevados pueden indicar infección viral o leucemia linfocítica.'
        ),
    },
    {
        'name': 'Monocitos', 'short_name': 'MONO', 'loinc_code': '742-7',
        'category': 'HEMATOLOGIA', 'unit': '10³/μL', 'order': 11,
        'ref_min_male': 0.1, 'ref_max_male': 1.2,
        'ref_min_female': 0.1, 'ref_max_female': 1.2,
        'low_is_bad': False,
        'description': 'Leucocitos que fagocitan patógenos y residuos celulares.',
    },
    {
        'name': 'Eosinófilos', 'short_name': 'EOS', 'loinc_code': '711-2',
        'category': 'HEMATOLOGIA', 'unit': '10³/μL', 'order': 12,
        'ref_min_male': 0.0, 'ref_max_male': 0.5,
        'ref_min_female': 0.0, 'ref_max_female': 0.5,
        'low_is_bad': False,
        'description': 'Elevados en alergias, asma y parasitosis.',
    },
    {
        'name': 'Basófilos', 'short_name': 'BASO', 'loinc_code': '704-7',
        'category': 'HEMATOLOGIA', 'unit': '10³/μL', 'order': 13,
        'ref_min_male': 0.0, 'ref_max_male': 0.1,
        'ref_min_female': 0.0, 'ref_max_female': 0.1,
        'low_is_bad': False,
        'description': 'El tipo de leucocito menos frecuente; interviene en reacciones alérgicas.',
    },
    {
        'name': 'Ancho de Distribución Eritrocitaria', 'short_name': 'RDW',
        'loinc_code': '788-0', 'category': 'HEMATOLOGIA', 'unit': '%', 'order': 14,
        'ref_min_male': 11.5, 'ref_max_male': 14.5,
        'ref_min_female': 11.5, 'ref_max_female': 14.5,
        'low_is_bad': False,
        'description': (
            'Mide la variabilidad en el tamaño de los glóbulos rojos. '
            'Elevado en anemias mixtas, deficiencias nutricionales o enfermedades crónicas. '
            'Es uno de los marcadores del algoritmo PhenoAge (Levine 2018).'
        ),
    },

    # ── BIOQUÍMICA ─────────────────────────────────────────────────────────────
    {
        'name': 'Glucosa', 'short_name': 'GLU', 'loinc_code': '2345-7',
        'category': 'BIOQUIMICA', 'unit': 'mg/dL', 'order': 1,
        'ref_min_male': 70.0, 'ref_max_male': 100.0,
        'ref_min_female': 70.0, 'ref_max_female': 100.0,
        'low_is_bad': False,
        'description': (
            'Nivel de azúcar en sangre en ayunas. '
            'Entre 100-125 mg/dL se considera prediabetes; '
            '≥ 126 mg/dL en dos ocasiones indica diabetes.'
        ),
    },
    {
        'name': 'Hemoglobina Glicosilada', 'short_name': 'HbA1c', 'loinc_code': '4548-4',
        'category': 'BIOQUIMICA', 'unit': '%', 'order': 2,
        'ref_min_male': 4.0, 'ref_max_male': 6.0,
        'ref_min_female': 4.0, 'ref_max_female': 6.0,
        'low_is_bad': False,
        'description': (
            'Refleja el nivel promedio de glucosa en los últimos 2-3 meses. '
            'Es el mejor indicador del control glucémico en diabéticos.'
        ),
    },
    {
        'name': 'Urea', 'short_name': 'UREA', 'loinc_code': '3091-6',
        'category': 'BIOQUIMICA', 'unit': 'mg/dL', 'order': 3,
        'ref_min_male': 15.0, 'ref_max_male': 45.0,
        'ref_min_female': 15.0, 'ref_max_female': 45.0,
        'low_is_bad': False,
        'description': (
            'Producto de desecho del metabolismo de proteínas, eliminado por los riñones. '
            'Valores altos pueden indicar insuficiencia renal o deshidratación.'
        ),
    },
    {
        'name': 'Creatinina', 'short_name': 'CREA', 'loinc_code': '2160-0',
        'category': 'BIOQUIMICA', 'unit': 'mg/dL', 'order': 4,
        'ref_min_male': 0.7, 'ref_max_male': 1.2,
        'ref_min_female': 0.5, 'ref_max_female': 1.0,
        'low_is_bad': False,
        'description': (
            'Indicador clave de la función renal. '
            'Se eleva cuando los riñones no filtran correctamente.'
        ),
    },
    {
        'name': 'Ácido Úrico', 'short_name': 'AU', 'loinc_code': '3084-1',
        'category': 'BIOQUIMICA', 'unit': 'mg/dL', 'order': 5,
        'ref_min_male': 3.4, 'ref_max_male': 7.2,
        'ref_min_female': 2.4, 'ref_max_female': 5.7,
        'low_is_bad': False,
        'description': (
            'Producto del metabolismo de las purinas. '
            'Valores elevados (hiperuricemia) pueden causar gota o cálculos renales.'
        ),
    },
    {
        'name': 'Bilirrubina Total', 'short_name': 'BILI', 'loinc_code': '1975-2',
        'category': 'BIOQUIMICA', 'unit': 'mg/dL', 'order': 6,
        'ref_min_male': 0.2, 'ref_max_male': 1.2,
        'ref_min_female': 0.2, 'ref_max_female': 1.2,
        'low_is_bad': False,
        'description': (
            'Pigmento resultante de la degradación de la hemoglobina. '
            'Valores altos provocan ictericia y pueden indicar problemas hepáticos o hemólisis.'
        ),
    },
    {
        'name': 'Proteínas Totales', 'short_name': 'PROT', 'loinc_code': '2885-2',
        'category': 'BIOQUIMICA', 'unit': 'g/dL', 'order': 7,
        'ref_min_male': 6.4, 'ref_max_male': 8.2,
        'ref_min_female': 6.4, 'ref_max_female': 8.2,
        'low_is_bad': True,
        'description': 'Suma de albúmina y globulinas en sangre. Valora el estado nutricional y la función hepática.',
    },
    {
        'name': 'Albúmina', 'short_name': 'ALB', 'loinc_code': '1751-7',
        'category': 'BIOQUIMICA', 'unit': 'g/dL', 'order': 8,
        'ref_min_male': 3.5, 'ref_max_male': 5.0,
        'ref_min_female': 3.5, 'ref_max_female': 5.0,
        'low_is_bad': True,
        'description': (
            'La proteína más abundante en el plasma. '
            'Niveles bajos indican malnutrición o hepatopatía grave.'
        ),
    },
    {
        'name': 'AST (GOT)', 'short_name': 'AST', 'loinc_code': '1920-8',
        'category': 'BIOQUIMICA', 'unit': 'U/L', 'order': 9,
        'ref_min_male': 10.0, 'ref_max_male': 40.0,
        'ref_min_female': 10.0, 'ref_max_female': 35.0,
        'low_is_bad': False,
        'description': (
            'Enzima hepática (y muscular). '
            'Elevada en daño hepático, infarto de miocardio o lesión muscular intensa.'
        ),
    },
    {
        'name': 'ALT (GPT)', 'short_name': 'ALT', 'loinc_code': '1742-6',
        'category': 'BIOQUIMICA', 'unit': 'U/L', 'order': 10,
        'ref_min_male': 10.0, 'ref_max_male': 45.0,
        'ref_min_female': 10.0, 'ref_max_female': 35.0,
        'low_is_bad': False,
        'description': (
            'Enzima específicamente hepática. '
            'Es el mejor indicador de daño en las células del hígado.'
        ),
    },
    {
        'name': 'GGT', 'short_name': 'GGT', 'loinc_code': '2324-2',
        'category': 'BIOQUIMICA', 'unit': 'U/L', 'order': 11,
        'ref_min_male': 9.0, 'ref_max_male': 48.0,
        'ref_min_female': 9.0, 'ref_max_female': 32.0,
        'low_is_bad': False,
        'description': (
            'Enzima hepática muy sensible al consumo de alcohol y al daño biliar. '
            'Suele elevarse antes que AST y ALT.'
        ),
    },
    {
        'name': 'Fosfatasa Alcalina', 'short_name': 'FA', 'loinc_code': '6768-6',
        'category': 'BIOQUIMICA', 'unit': 'U/L', 'order': 12,
        'ref_min_male': 40.0, 'ref_max_male': 130.0,
        'ref_min_female': 40.0, 'ref_max_female': 130.0,
        'low_is_bad': False,
        'description': (
            'Enzima presente en hígado, huesos, riñones e intestino. '
            'Se eleva en enfermedades hepáticas, óseas o de las vías biliares.'
        ),
    },

    # ── LÍPIDOS ────────────────────────────────────────────────────────────────
    {
        'name': 'Colesterol Total', 'short_name': 'COL', 'loinc_code': '2093-3',
        'category': 'LIPIDOS', 'unit': 'mg/dL', 'order': 1,
        'ref_min_male': None, 'ref_max_male': 200.0,
        'ref_min_female': None, 'ref_max_female': 200.0,
        'low_is_bad': False,
        'description': (
            'Suma de todo el colesterol en sangre. '
            'Por encima de 200 mg/dL aumenta el riesgo cardiovascular.'
        ),
    },
    {
        'name': 'Colesterol HDL', 'short_name': 'HDL', 'loinc_code': '2085-9',
        'category': 'LIPIDOS', 'unit': 'mg/dL', 'order': 2,
        'ref_min_male': 40.0, 'ref_max_male': None,
        'ref_min_female': 50.0, 'ref_max_female': None,
        'low_is_bad': True,
        'description': (
            'Colesterol "bueno". Transporta el colesterol de las arterias al hígado. '
            'Valores altos son protectores; valores bajos aumentan el riesgo cardiovascular.'
        ),
    },
    {
        'name': 'Colesterol LDL', 'short_name': 'LDL', 'loinc_code': '2089-1',
        'category': 'LIPIDOS', 'unit': 'mg/dL', 'order': 3,
        'ref_min_male': None, 'ref_max_male': 130.0,
        'ref_min_female': None, 'ref_max_female': 130.0,
        'low_is_bad': False,
        'description': (
            'Colesterol "malo". Se deposita en las arterias favoreciendo la aterosclerosis. '
            'El objetivo es mantenerlo lo más bajo posible.'
        ),
    },
    {
        'name': 'Triglicéridos', 'short_name': 'TG', 'loinc_code': '2571-8',
        'category': 'LIPIDOS', 'unit': 'mg/dL', 'order': 4,
        'ref_min_male': None, 'ref_max_male': 150.0,
        'ref_min_female': None, 'ref_max_female': 150.0,
        'low_is_bad': False,
        'description': (
            'Tipo de grasa presente en sangre. '
            'Elevados se asocian a obesidad, diabetes y mayor riesgo cardiovascular.'
        ),
    },
    {
        'name': 'Índice Aterogénico', 'short_name': 'IA', 'loinc_code': '',
        'category': 'LIPIDOS', 'unit': 'ratio', 'order': 5,
        'ref_min_male': None, 'ref_max_male': 5.0,
        'ref_min_female': None, 'ref_max_female': 4.5,
        'low_is_bad': False,
        'description': (
            'Cociente Colesterol Total / HDL. '
            'Estima el riesgo cardiovascular: cuanto más bajo, mejor.'
        ),
    },

    # ── TIROIDES ───────────────────────────────────────────────────────────────
    {
        'name': 'TSH', 'short_name': 'TSH', 'loinc_code': '3016-3',
        'category': 'TIROIDES', 'unit': 'mUI/L', 'order': 1,
        'ref_min_male': 0.4, 'ref_max_male': 4.0,
        'ref_min_female': 0.4, 'ref_max_female': 4.0,
        'low_is_bad': False,
        'description': (
            'Hormona estimulante del tiroides. '
            'Baja en hipertiroidismo; alta en hipotiroidismo. '
            'Es el mejor cribado de función tiroidea.'
        ),
    },
    {
        'name': 'T4 Libre', 'short_name': 'T4L', 'loinc_code': '3024-7',
        'category': 'TIROIDES', 'unit': 'ng/dL', 'order': 2,
        'ref_min_male': 0.8, 'ref_max_male': 1.8,
        'ref_min_female': 0.8, 'ref_max_female': 1.8,
        'low_is_bad': True,
        'description': (
            'Tiroxina libre, la hormona tiroidea activa más importante. '
            'Baja en hipotiroidismo; alta en hipertiroidismo.'
        ),
    },

    # ── HIERRO ─────────────────────────────────────────────────────────────────
    {
        'name': 'Hierro Sérico', 'short_name': 'FE', 'loinc_code': '2498-4',
        'category': 'HIERRO', 'unit': 'μg/dL', 'order': 1,
        'ref_min_male': 65.0, 'ref_max_male': 175.0,
        'ref_min_female': 50.0, 'ref_max_female': 170.0,
        'low_is_bad': True,
        'description': 'Cantidad de hierro circulando en la sangre. Varía mucho a lo largo del día.',
    },
    {
        'name': 'Ferritina', 'short_name': 'FERR', 'loinc_code': '2276-4',
        'category': 'HIERRO', 'unit': 'ng/mL', 'order': 2,
        'ref_min_male': 30.0, 'ref_max_male': 300.0,
        'ref_min_female': 12.0, 'ref_max_female': 150.0,
        'low_is_bad': True,
        'description': (
            'Proteína de almacenamiento de hierro. '
            'Es el mejor indicador de las reservas de hierro del organismo. '
            'Valores bajos indican déficit de hierro antes de que aparezca anemia.'
        ),
    },
    {
        'name': 'Transferrina', 'short_name': 'TRANSF', 'loinc_code': '3034-6',
        'category': 'HIERRO', 'unit': 'mg/dL', 'order': 3,
        'ref_min_male': 200.0, 'ref_max_male': 360.0,
        'ref_min_female': 200.0, 'ref_max_female': 360.0,
        'low_is_bad': True,
        'description': 'Proteína transportadora de hierro. Aumenta cuando hay déficit de hierro.',
    },
    {
        'name': 'Saturación de Transferrina', 'short_name': 'SATFE', 'loinc_code': '2502-3',
        'category': 'HIERRO', 'unit': '%', 'order': 4,
        'ref_min_male': 20.0, 'ref_max_male': 50.0,
        'ref_min_female': 20.0, 'ref_max_female': 50.0,
        'low_is_bad': True,
        'description': 'Porcentaje de transferrina que está cargada de hierro.',
    },
    {
        'name': 'TIBC', 'short_name': 'TIBC', 'loinc_code': '2500-7',
        'category': 'HIERRO', 'unit': 'μg/dL', 'order': 5,
        'ref_min_male': 250.0, 'ref_max_male': 370.0,
        'ref_min_female': 250.0, 'ref_max_female': 370.0,
        'low_is_bad': False,
        'description': 'Capacidad total de fijación del hierro. Aumenta en deficiencia de hierro.',
    },

    # ── INFLAMACIÓN ────────────────────────────────────────────────────────────
    {
        'name': 'Proteína C Reactiva', 'short_name': 'PCR', 'loinc_code': '1988-5',
        'category': 'INFLAMACION', 'unit': 'mg/L', 'order': 1,
        'ref_min_male': None, 'ref_max_male': 5.0,
        'ref_min_female': None, 'ref_max_female': 5.0,
        'low_is_bad': False,
        'description': (
            'Marcador de inflamación aguda. '
            'Se eleva rápidamente ante infecciones, traumatismos o inflamación sistémica.'
        ),
    },
    {
        'name': 'Velocidad de Sedimentación Globular', 'short_name': 'VSG', 'loinc_code': '4537-7',
        'category': 'INFLAMACION', 'unit': 'mm/h', 'order': 2,
        'ref_min_male': None, 'ref_max_male': 15.0,
        'ref_min_female': None, 'ref_max_female': 20.0,
        'low_is_bad': False,
        'description': (
            'Velocidad a la que los glóbulos rojos se sedimentan en una hora. '
            'Indicador inespecífico de inflamación crónica.'
        ),
    },
    {
        'name': 'Fibrinógeno', 'short_name': 'FIBR', 'loinc_code': '3255-7',
        'category': 'INFLAMACION', 'unit': 'mg/dL', 'order': 3,
        'ref_min_male': 200.0, 'ref_max_male': 400.0,
        'ref_min_female': 200.0, 'ref_max_female': 400.0,
        'low_is_bad': True,
        'description': (
            'Proteína de la coagulación y reactante de fase aguda. '
            'Elevado en inflamación crónica y factor de riesgo cardiovascular.'
        ),
    },

    # ── ORINA ──────────────────────────────────────────────────────────────────
    {
        'name': 'pH Urinario', 'short_name': 'pH', 'loinc_code': '2756-5',
        'category': 'ORINA', 'unit': '', 'order': 1,
        'ref_min_male': 5.0, 'ref_max_male': 8.0,
        'ref_min_female': 5.0, 'ref_max_female': 8.0,
        'low_is_bad': False,
        'description': 'Acidez de la orina. Varía con la dieta y el estado de hidratación.',
    },
    {
        'name': 'Densidad Urinaria', 'short_name': 'DENS', 'loinc_code': '5811-5',
        'category': 'ORINA', 'unit': '', 'order': 2,
        'ref_min_male': 1.005, 'ref_max_male': 1.030,
        'ref_min_female': 1.005, 'ref_max_female': 1.030,
        'low_is_bad': False,
        'description': 'Indica la capacidad del riñón para concentrar la orina.',
    },
    {
        'name': 'Glucosa en Orina', 'short_name': 'GLU-U', 'loinc_code': '2349-9',
        'category': 'ORINA', 'unit': 'mg/dL', 'order': 3,
        'ref_min_male': None, 'ref_max_male': 15.0,
        'ref_min_female': None, 'ref_max_female': 15.0,
        'low_is_bad': False,
        'description': 'Glucosa en orina. Aparece cuando la glucemia supera el umbral renal (~180 mg/dL).',
    },
    {
        'name': 'Proteínas en Orina', 'short_name': 'PROT-U', 'loinc_code': '2888-6',
        'category': 'ORINA', 'unit': 'mg/dL', 'order': 4,
        'ref_min_male': None, 'ref_max_male': 14.0,
        'ref_min_female': None, 'ref_max_female': 14.0,
        'low_is_bad': False,
        'description': (
            'Proteínas en orina. Su presencia persistente (proteinuria) puede indicar '
            'daño renal o hipertensión.'
        ),
    },
    {
        'name': 'Leucocitos en Orina', 'short_name': 'LEU-U', 'loinc_code': '5821-4',
        'category': 'ORINA', 'unit': '/campo', 'order': 5,
        'ref_min_male': None, 'ref_max_male': 5.0,
        'ref_min_female': None, 'ref_max_female': 5.0,
        'low_is_bad': False,
        'description': 'Leucocitos en sedimento urinario. Elevados sugieren infección urinaria.',
    },
    {
        'name': 'Hematíes en Orina', 'short_name': 'HEM-U', 'loinc_code': '13945-1',
        'category': 'ORINA', 'unit': '/campo', 'order': 6,
        'ref_min_male': None, 'ref_max_male': 2.0,
        'ref_min_female': None, 'ref_max_female': 3.0,
        'low_is_bad': False,
        'description': 'Glóbulos rojos en orina. Más de 3/campo puede indicar litiasis, infección o patología renal.',
    },
    {
        'name': 'Cuerpos Cetónicos en Orina', 'short_name': 'CET-U', 'loinc_code': '2514-8',
        'category': 'ORINA', 'unit': 'mg/dL', 'order': 7,
        'ref_min_male': None, 'ref_max_male': 0.0,
        'ref_min_female': None, 'ref_max_female': 0.0,
        'low_is_bad': False,
        'description': 'Cetonas en orina. Aparecen en ayuno prolongado, dietas cetogénicas o cetoacidosis diabética.',
    },

    # ── VITAMINAS ──────────────────────────────────────────────────────────────
    {
        'name': 'Vitamina D (25-OH)', 'short_name': 'VIT-D', 'loinc_code': '1989-3',
        'category': 'VITAMINAS', 'unit': 'ng/mL', 'order': 1,
        'ref_min_male': 30.0, 'ref_max_male': 100.0,
        'ref_min_female': 30.0, 'ref_max_female': 100.0,
        'low_is_bad': True,
        'description': (
            'La vitamina del sol. Esencial para la absorción de calcio, '
            'la función inmune y la salud ósea. '
            'Deficiencia muy frecuente en España (< 20 ng/mL).'
        ),
    },
    {
        'name': 'Vitamina B12', 'short_name': 'B12', 'loinc_code': '2132-9',
        'category': 'VITAMINAS', 'unit': 'pg/mL', 'order': 2,
        'ref_min_male': 200.0, 'ref_max_male': 900.0,
        'ref_min_female': 200.0, 'ref_max_female': 900.0,
        'low_is_bad': True,
        'description': (
            'Esencial para la formación de glóbulos rojos y el sistema nervioso. '
            'Su déficit causa anemia megaloblástica y neuropatía. '
            'Riesgo en veganos y personas mayores.'
        ),
    },
    {
        'name': 'Ácido Fólico', 'short_name': 'FOL', 'loinc_code': '2284-8',
        'category': 'VITAMINAS', 'unit': 'ng/mL', 'order': 3,
        'ref_min_male': 3.0, 'ref_max_male': 17.0,
        'ref_min_female': 3.0, 'ref_max_female': 17.0,
        'low_is_bad': True,
        'description': (
            'Vitamina B9. Fundamental para la síntesis de ADN y la formación de glóbulos rojos. '
            'Crítico en el embarazo para prevenir defectos del tubo neural.'
        ),
    },

    # ── OTRO ───────────────────────────────────────────────────────────────────
    {
        'name': 'PSA Total', 'short_name': 'PSA', 'loinc_code': '2857-1',
        'category': 'OTRO', 'unit': 'ng/mL', 'order': 1,
        'ref_min_male': None, 'ref_max_male': 4.0,
        'ref_min_female': None, 'ref_max_female': None,
        'low_is_bad': False,
        'description': (
            'Antígeno prostático específico (solo hombres). '
            'Se usa para el cribado de cáncer de próstata. '
            'Puede elevarse también por hiperplasia benigna o prostatitis.'
        ),
    },
    {
        'name': 'Calcio', 'short_name': 'CA', 'loinc_code': '17861-6',
        'category': 'OTRO', 'unit': 'mg/dL', 'order': 2,
        'ref_min_male': 8.5, 'ref_max_male': 10.5,
        'ref_min_female': 8.5, 'ref_max_female': 10.5,
        'low_is_bad': True,
        'description': (
            'Mineral esencial para huesos, dientes, nervios y músculos. '
            'Hipocalcemia e hipercalcemia tienen consecuencias serias.'
        ),
    },
    {
        'name': 'Fósforo', 'short_name': 'P', 'loinc_code': '2777-1',
        'category': 'OTRO', 'unit': 'mg/dL', 'order': 3,
        'ref_min_male': 2.5, 'ref_max_male': 4.5,
        'ref_min_female': 2.5, 'ref_max_female': 4.5,
        'low_is_bad': True,
        'description': 'Trabaja junto al calcio en la salud ósea y muscular.',
    },
    {
        'name': 'Sodio', 'short_name': 'NA', 'loinc_code': '2951-2',
        'category': 'OTRO', 'unit': 'mEq/L', 'order': 4,
        'ref_min_male': 136.0, 'ref_max_male': 145.0,
        'ref_min_female': 136.0, 'ref_max_female': 145.0,
        'low_is_bad': True,
        'description': (
            'Electrolito principal del líquido extracelular. '
            'Regula el equilibrio hídrico y la tensión arterial.'
        ),
    },
    {
        'name': 'Potasio', 'short_name': 'K', 'loinc_code': '2823-3',
        'category': 'OTRO', 'unit': 'mEq/L', 'order': 5,
        'ref_min_male': 3.5, 'ref_max_male': 5.1,
        'ref_min_female': 3.5, 'ref_max_female': 5.1,
        'low_is_bad': True,
        'description': (
            'Electrolito clave en la función cardíaca y muscular. '
            'Hipopotasemia e hiperpotasemia pueden causar arritmias.'
        ),
    },
    {
        'name': 'Cloro', 'short_name': 'CL', 'loinc_code': '2075-0',
        'category': 'OTRO', 'unit': 'mEq/L', 'order': 6,
        'ref_min_male': 98.0, 'ref_max_male': 107.0,
        'ref_min_female': 98.0, 'ref_max_female': 107.0,
        'low_is_bad': True,
        'description': 'Electrolito que mantiene el equilibrio ácido-base y la osmolaridad plasmática.',
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
                short_name=data['short_name'],
                category=data['category'],
                defaults={
                    'name': data['name'],
                    'loinc_code': data.get('loinc_code', ''),
                    'unit': data['unit'],
                    'description': data.get('description', ''),
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
