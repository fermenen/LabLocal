"""
Traducciones de biomarcadores indexadas por LOINC code.

Los nombres, abreviaturas y descripciones clínicas viven aquí, fuera de la base
de datos, de modo que la BD solo almacena datos científicos puros (unidades,
rangos de referencia, etc.).

Añadir un idioma nuevo:
  1. Añadir una clave de idioma a cada entrada (p. ej. 'fr': {...}).
  2. Ejecutar compilemessages si se usan cadenas .po para la UI.
"""

from django.utils.translation import get_language

# ---------------------------------------------------------------------------
# Catálogo principal
# ---------------------------------------------------------------------------

_T = {

    # ── HEMATOLOGÍA ──────────────────────────────────────────────────────────

    '6690-2': {
        'en': {
            'name': 'Leukocytes',
            'short_name': 'WBC',
            'description': (
                'White blood cell count — total leukocytes per unit volume in whole blood. '
                'Elevated values may indicate infection or inflammation; '
                'low values may indicate immunosuppression.'
            ),
        },
        'es': {
            'name': 'Leucocitos',
            'short_name': 'Leucocitos',
            'description': (
                'Glóbulos blancos. Son las células del sistema inmune. '
                'Valores altos pueden indicar infección o inflamación; '
                'valores bajos pueden indicar inmunosupresión.'
            ),
        },
        'pt': {
            'name': 'Leucócitos',
            'short_name': 'Leucócitos',
            'description': (
                'Glóbulos brancos. São as células do sistema imunológico. '
                'Valores elevados podem indicar infecção ou inflamação; '
                'valores baixos podem indicar imunossupressão.'
            ),
        },
    },

    '789-8': {
        'en': {
            'name': 'Erythrocytes',
            'short_name': 'RBC',
            'description': (
                'Red blood cell count by automated analyzer. '
                'Core component of the CBC; low values indicate anemia.'
            ),
        },
        'es': {
            'name': 'Eritrocitos',
            'short_name': 'Eritrocitos',
            'description': (
                'Glóbulos rojos. Transportan oxígeno desde los pulmones al resto del cuerpo. '
                'Su recuento bajo puede indicar anemia.'
            ),
        },
        'pt': {
            'name': 'Eritrócitos',
            'short_name': 'Eritrócitos',
            'description': (
                'Glóbulos vermelhos. Transportam oxigênio dos pulmões para o restante do corpo. '
                'Contagem baixa pode indicar anemia.'
            ),
        },
    },

    '718-7': {
        'en': {
            'name': 'Hemoglobin',
            'short_name': 'Hgb',
            'description': (
                'Concentration of hemoglobin in whole blood. '
                'Primary indicator for diagnosing anemia and polycythemia.'
            ),
        },
        'es': {
            'name': 'Hemoglobina',
            'short_name': 'Hb',
            'description': (
                'Proteína dentro de los glóbulos rojos que transporta el oxígeno. '
                'Es el principal indicador de anemia.'
            ),
        },
        'pt': {
            'name': 'Hemoglobina',
            'short_name': 'Hb',
            'description': (
                'Proteína dentro dos glóbulos vermelhos que transporta oxigênio. '
                'É o principal indicador de anemia.'
            ),
        },
    },

    '4544-3': {
        'en': {
            'name': 'Hematocrit',
            'short_name': 'Hct',
            'description': (
                'Proportion of blood volume occupied by red blood cells, measured by automated analyzer. '
                'Complements hemoglobin to evaluate anemia.'
            ),
        },
        'es': {
            'name': 'Hematocrito',
            'short_name': 'Hto',
            'description': (
                'Porcentaje del volumen sanguíneo ocupado por glóbulos rojos. '
                'Complementa a la hemoglobina para valorar la anemia.'
            ),
        },
        'pt': {
            'name': 'Hematócrito',
            'short_name': 'Ht',
            'description': (
                'Percentagem do volume sanguíneo ocupado pelos glóbulos vermelhos. '
                'Complementa a hemoglobina na avaliação da anemia.'
            ),
        },
    },

    '787-2': {
        'en': {
            'name': 'Mean Corpuscular Volume',
            'short_name': 'MCV',
            'description': (
                'Average volume of a red blood cell. '
                'Low values (microcytosis) suggest iron deficiency; '
                'high values (macrocytosis) suggest B12 or folate deficiency.'
            ),
        },
        'es': {
            'name': 'Volumen Corpuscular Medio',
            'short_name': 'VCM',
            'description': (
                'Tamaño medio de los glóbulos rojos. '
                'Valores bajos (microcitosis) se asocian con deficiencia de hierro; '
                'valores altos (macrocitosis) con deficiencia de B12 o folato.'
            ),
        },
        'pt': {
            'name': 'Volume Corpuscular Médio',
            'short_name': 'VCM',
            'description': (
                'Tamanho médio dos glóbulos vermelhos. '
                'Valores baixos (microcitose) associam-se a deficiência de ferro; '
                'valores altos (macrocitose) a deficiência de B12 ou folato.'
            ),
        },
    },

    '785-6': {
        'en': {
            'name': 'Mean Corpuscular Hemoglobin',
            'short_name': 'MCH',
            'description': 'Average mass of hemoglobin per red blood cell. Useful in the differential diagnosis of anemia.',
        },
        'es': {
            'name': 'Hemoglobina Corpuscular Media',
            'short_name': 'HCM',
            'description': 'Cantidad media de hemoglobina por glóbulo rojo.',
        },
        'pt': {
            'name': 'Hemoglobina Corpuscular Média',
            'short_name': 'HCM',
            'description': 'Quantidade média de hemoglobina por glóbulo vermelho.',
        },
    },

    '786-4': {
        'en': {
            'name': 'Mean Corpuscular Hemoglobin Concentration',
            'short_name': 'MCHC',
            'description': (
                'Average concentration of hemoglobin in a given volume of packed red blood cells. '
                'Elevated in spherocytosis; decreased in iron-deficiency anemia.'
            ),
        },
        'es': {
            'name': 'Concentración de Hemoglobina Corpuscular Media',
            'short_name': 'CHCM',
            'description': 'Concentración de hemoglobina en relación al volumen del glóbulo rojo.',
        },
        'pt': {
            'name': 'Concentração de Hemoglobina Corpuscular Média',
            'short_name': 'CHCM',
            'description': 'Concentração de hemoglobina em relação ao volume do glóbulo vermelho.',
        },
    },

    '777-3': {
        'en': {
            'name': 'Platelets',
            'short_name': 'PLT',
            'description': (
                'Platelet count by automated analyzer. '
                'Low values increase bleeding risk; high values may be associated with thrombosis.'
            ),
        },
        'es': {
            'name': 'Plaquetas',
            'short_name': 'Plaquetas',
            'description': (
                'Fragmentos celulares implicados en la coagulación. '
                'Valores bajos aumentan el riesgo de hemorragia; '
                'valores altos pueden asociarse a trombosis.'
            ),
        },
        'pt': {
            'name': 'Plaquetas',
            'short_name': 'Plaquetas',
            'description': (
                'Fragmentos celulares envolvidos na coagulação. '
                'Valores baixos aumentam o risco de hemorragia; '
                'valores altos podem associar-se a trombose.'
            ),
        },
    },

    '751-8': {
        'en': {
            'name': 'Neutrophils',
            'short_name': 'NEUT',
            'description': (
                'Absolute neutrophil count by automated analyzer. '
                'Key indicator of infection susceptibility; elevated in bacterial infections.'
            ),
        },
        'es': {
            'name': 'Neutrófilos',
            'short_name': 'Neutrófilos',
            'description': (
                'Tipo de leucocito, primera línea de defensa contra infecciones bacterianas. '
                'Su aumento (neutrofilia) suele indicar infección aguda.'
            ),
        },
        'pt': {
            'name': 'Neutrófilos',
            'short_name': 'Neutrófilos',
            'description': (
                'Tipo de leucócito, primeira linha de defesa contra infecções bacterianas. '
                'O aumento (neutrofilia) costuma indicar infecção aguda.'
            ),
        },
    },

    '731-0': {
        'en': {
            'name': 'Lymphocytes',
            'short_name': 'LYMPH',
            'description': (
                'Absolute lymphocyte count. '
                'Elevated in viral infections and lymphomas; decreased in HIV and immunodeficiency.'
            ),
        },
        'es': {
            'name': 'Linfocitos',
            'short_name': 'Linfocitos',
            'description': (
                'Leucocitos clave en la respuesta inmune adaptativa. '
                'Muy elevados pueden indicar infección viral o leucemia linfocítica.'
            ),
        },
        'pt': {
            'name': 'Linfócitos',
            'short_name': 'Linfócitos',
            'description': (
                'Leucócitos chave na resposta imune adaptativa. '
                'Muito elevados podem indicar infecção viral ou leucemia linfocítica.'
            ),
        },
    },

    '742-7': {
        'en': {
            'name': 'Monocytes',
            'short_name': 'MONO',
            'description': 'Absolute monocyte count. Elevated in chronic infections, autoimmune diseases, and certain hematologic malignancies.',
        },
        'es': {
            'name': 'Monocitos',
            'short_name': 'Monocitos',
            'description': 'Leucocitos que fagocitan patógenos y residuos celulares.',
        },
        'pt': {
            'name': 'Monócitos',
            'short_name': 'Monócitos',
            'description': 'Leucócitos que fagocitam patógenos e resíduos celulares.',
        },
    },

    '711-2': {
        'en': {
            'name': 'Eosinophils',
            'short_name': 'EOS',
            'description': 'Absolute eosinophil count. Elevated in allergic conditions, parasitic infections, and eosinophilic disorders.',
        },
        'es': {
            'name': 'Eosinófilos',
            'short_name': 'Eosinófilos',
            'description': 'Elevados en alergias, asma y parasitosis.',
        },
        'pt': {
            'name': 'Eosinófilos',
            'short_name': 'Eosinófilos',
            'description': 'Elevados em alergias, asma e parasitoses.',
        },
    },

    '704-7': {
        'en': {
            'name': 'Basophils',
            'short_name': 'BASO',
            'description': 'Absolute basophil count. The least frequent leukocyte type; involved in allergic reactions and myeloproliferative disorders.',
        },
        'es': {
            'name': 'Basófilos',
            'short_name': 'Basófilos',
            'description': 'El tipo de leucocito menos frecuente; interviene en reacciones alérgicas.',
        },
        'pt': {
            'name': 'Basófilos',
            'short_name': 'Basófilos',
            'description': 'O tipo de leucócito menos frequente; participa em reações alérgicas.',
        },
    },

    '788-0': {
        'en': {
            'name': 'Red Cell Distribution Width',
            'short_name': 'RDW',
            'description': (
                'Measure of variation in red blood cell size (anisocytosis). '
                'Elevated in iron-deficiency anemia, B12/folate deficiency, and mixed anemias. '
                'One of the markers in the PhenoAge algorithm (Levine 2018).'
            ),
        },
        'es': {
            'name': 'Ancho de Distribución Eritrocitaria',
            'short_name': 'ADE',
            'description': (
                'Mide la variabilidad en el tamaño de los glóbulos rojos. '
                'Elevado en anemias mixtas, deficiencias nutricionales o enfermedades crónicas. '
                'Es uno de los marcadores del algoritmo PhenoAge (Levine 2018).'
            ),
        },
        'pt': {
            'name': 'Amplitude de Distribuição Eritrocitária',
            'short_name': 'ADE',
            'description': (
                'Mede a variabilidade no tamanho dos glóbulos vermelhos. '
                'Elevada em anemias mistas, deficiências nutricionais ou doenças crónicas. '
                'É um dos marcadores do algoritmo PhenoAge (Levine 2018).'
            ),
        },
    },

    # ── BIOQUÍMICA ───────────────────────────────────────────────────────────

    '2345-7': {
        'en': {
            'name': 'Glucose',
            'short_name': 'GLU',
            'description': (
                'Fasting blood glucose. '
                '100–125 mg/dL is considered pre-diabetes; '
                '≥ 126 mg/dL on two occasions indicates diabetes.'
            ),
        },
        'es': {
            'name': 'Glucosa',
            'short_name': 'Glucosa',
            'description': (
                'Nivel de azúcar en sangre en ayunas. '
                'Entre 100-125 mg/dL se considera prediabetes; '
                '≥ 126 mg/dL en dos ocasiones indica diabetes.'
            ),
        },
        'pt': {
            'name': 'Glicose',
            'short_name': 'Glicose',
            'description': (
                'Nível de açúcar no sangue em jejum. '
                'Entre 100-125 mg/dL considera-se pré-diabetes; '
                '≥ 126 mg/dL em duas ocasiões indica diabetes.'
            ),
        },
    },

    '4548-4': {
        'en': {
            'name': 'Glycated Hemoglobin',
            'short_name': 'HbA1c',
            'description': (
                'Reflects average blood glucose over the preceding 2–3 months. '
                'Primary marker for long-term glycemic control in diabetes.'
            ),
        },
        'es': {
            'name': 'Hemoglobina Glicosilada',
            'short_name': 'HbA1c',
            'description': (
                'Refleja el nivel promedio de glucosa en los últimos 2-3 meses. '
                'Es el mejor indicador del control glucémico en diabéticos.'
            ),
        },
        'pt': {
            'name': 'Hemoglobina Glicada',
            'short_name': 'HbA1c',
            'description': (
                'Reflete o nível médio de glicose nos últimos 2-3 meses. '
                'É o melhor indicador do controle glicêmico em diabéticos.'
            ),
        },
    },

    '3091-6': {
        'en': {
            'name': 'Urea',
            'short_name': 'BUN',
            'description': (
                'Blood urea nitrogen — waste product of protein metabolism eliminated by the kidneys. '
                'Elevated values may indicate renal insufficiency or dehydration.'
            ),
        },
        'es': {
            'name': 'Urea',
            'short_name': 'Urea',
            'description': (
                'Producto de desecho del metabolismo de proteínas, eliminado por los riñones. '
                'Valores altos pueden indicar insuficiencia renal o deshidratación.'
            ),
        },
        'pt': {
            'name': 'Ureia',
            'short_name': 'Ureia',
            'description': (
                'Produto residual do metabolismo de proteínas, eliminado pelos rins. '
                'Valores elevados podem indicar insuficiência renal ou desidratação.'
            ),
        },
    },

    '2160-0': {
        'en': {
            'name': 'Creatinine',
            'short_name': 'Creat',
            'description': (
                'Key indicator of renal function. '
                'Rises when the kidneys do not filter correctly.'
            ),
        },
        'es': {
            'name': 'Creatinina',
            'short_name': 'Creatinina',
            'description': (
                'Indicador clave de la función renal. '
                'Se eleva cuando los riñones no filtran correctamente.'
            ),
        },
        'pt': {
            'name': 'Creatinina',
            'short_name': 'Creatinina',
            'description': (
                'Indicador chave da função renal. '
                'Eleva-se quando os rins não filtram corretamente.'
            ),
        },
    },

    '3084-1': {
        'en': {
            'name': 'Uric Acid',
            'short_name': 'UA',
            'description': (
                'Product of purine metabolism. '
                'Elevated levels (hyperuricemia) can cause gout or kidney stones.'
            ),
        },
        'es': {
            'name': 'Ácido Úrico',
            'short_name': 'Ác. Úrico',
            'description': (
                'Producto del metabolismo de las purinas. '
                'Valores elevados (hiperuricemia) pueden causar gota o cálculos renales.'
            ),
        },
        'pt': {
            'name': 'Ácido Úrico',
            'short_name': 'Ác. Úrico',
            'description': (
                'Produto do metabolismo das purinas. '
                'Valores elevados (hiperuricemia) podem causar gota ou cálculos renais.'
            ),
        },
    },

    '1975-2': {
        'en': {
            'name': 'Total Bilirubin',
            'short_name': 'T-Bili',
            'description': (
                'Pigment resulting from hemoglobin degradation. '
                'Elevated values cause jaundice and may indicate liver disease or hemolysis.'
            ),
        },
        'es': {
            'name': 'Bilirrubina Total',
            'short_name': 'Bilirrubina',
            'description': (
                'Pigmento resultante de la degradación de la hemoglobina. '
                'Valores altos provocan ictericia y pueden indicar problemas hepáticos o hemólisis.'
            ),
        },
        'pt': {
            'name': 'Bilirrubina Total',
            'short_name': 'Bilirrubina',
            'description': (
                'Pigmento resultante da degradação da hemoglobina. '
                'Valores elevados causam icterícia e podem indicar problemas hepáticos ou hemólise.'
            ),
        },
    },

    '2885-2': {
        'en': {
            'name': 'Total Protein',
            'short_name': 'TP',
            'description': (
                'Sum of albumin and globulins in serum. '
                'Assesses nutritional status and liver function.'
            ),
        },
        'es': {
            'name': 'Proteínas Totales',
            'short_name': 'Proteínas',
            'description': 'Suma de albúmina y globulinas en sangre. Valora el estado nutricional y la función hepática.',
        },
        'pt': {
            'name': 'Proteínas Totais',
            'short_name': 'Proteínas',
            'description': 'Soma de albumina e globulinas no sangue. Avalia o estado nutricional e a função hepática.',
        },
    },

    '1751-7': {
        'en': {
            'name': 'Albumin',
            'short_name': 'Alb',
            'description': (
                'The most abundant plasma protein. '
                'Low levels indicate malnutrition or severe liver disease.'
            ),
        },
        'es': {
            'name': 'Albúmina',
            'short_name': 'Albúmina',
            'description': (
                'La proteína más abundante en el plasma. '
                'Niveles bajos indican malnutrición o hepatopatía grave.'
            ),
        },
        'pt': {
            'name': 'Albumina',
            'short_name': 'Albumina',
            'description': (
                'A proteína mais abundante no plasma. '
                'Níveis baixos indicam desnutrição ou hepatopatia grave.'
            ),
        },
    },

    '1920-8': {
        'en': {
            'name': 'AST (GOT)',
            'short_name': 'AST',
            'description': (
                'Liver enzyme also present in muscle and heart. '
                'Elevated in hepatic damage, myocardial infarction, or intense muscle injury.'
            ),
        },
        'es': {
            'name': 'AST (GOT)',
            'short_name': 'AST',
            'description': (
                'Enzima hepática (y muscular). '
                'Elevada en daño hepático, infarto de miocardio o lesión muscular intensa.'
            ),
        },
        'pt': {
            'name': 'AST (TGO)',
            'short_name': 'AST',
            'description': (
                'Enzima hepática (e muscular). '
                'Elevada em dano hepático, infarto do miocárdio ou lesão muscular intensa.'
            ),
        },
    },

    '1742-6': {
        'en': {
            'name': 'ALT (GPT)',
            'short_name': 'ALT',
            'description': (
                'Liver-specific enzyme. '
                'The best indicator of hepatocellular damage.'
            ),
        },
        'es': {
            'name': 'ALT (GPT)',
            'short_name': 'ALT',
            'description': (
                'Enzima específicamente hepática. '
                'Es el mejor indicador de daño en las células del hígado.'
            ),
        },
        'pt': {
            'name': 'ALT (TGP)',
            'short_name': 'ALT',
            'description': (
                'Enzima especificamente hepática. '
                'É o melhor indicador de dano nas células do fígado.'
            ),
        },
    },

    '2324-2': {
        'en': {
            'name': 'GGT',
            'short_name': 'GGT',
            'description': (
                'Liver enzyme highly sensitive to alcohol consumption and biliary damage. '
                'Usually rises before AST and ALT.'
            ),
        },
        'es': {
            'name': 'GGT',
            'short_name': 'GGT',
            'description': (
                'Enzima hepática muy sensible al consumo de alcohol y al daño biliar. '
                'Suele elevarse antes que AST y ALT.'
            ),
        },
        'pt': {
            'name': 'GGT',
            'short_name': 'GGT',
            'description': (
                'Enzima hepática muito sensível ao consumo de álcool e dano biliar. '
                'Costuma elevar-se antes de AST e ALT.'
            ),
        },
    },

    '6768-6': {
        'en': {
            'name': 'Alkaline Phosphatase',
            'short_name': 'ALP',
            'description': (
                'Enzyme present in liver, bone, kidneys, and intestine. '
                'Elevated in liver disease, bone disorders, or biliary tract disease.'
            ),
        },
        'es': {
            'name': 'Fosfatasa Alcalina',
            'short_name': 'FA',
            'description': (
                'Enzima presente en hígado, huesos, riñones e intestino. '
                'Se eleva en enfermedades hepáticas, óseas o de las vías biliares.'
            ),
        },
        'pt': {
            'name': 'Fosfatase Alcalina',
            'short_name': 'FA',
            'description': (
                'Enzima presente no fígado, ossos, rins e intestino. '
                'Eleva-se em doenças hepáticas, ósseas ou das vias biliares.'
            ),
        },
    },

    # ── LÍPIDOS ──────────────────────────────────────────────────────────────

    '2093-3': {
        'en': {
            'name': 'Total Cholesterol',
            'short_name': 'Chol',
            'description': (
                'Sum of all cholesterol in the blood. '
                'Above 200 mg/dL increases cardiovascular risk.'
            ),
        },
        'es': {
            'name': 'Colesterol Total',
            'short_name': 'Colesterol',
            'description': (
                'Suma de todo el colesterol en sangre. '
                'Por encima de 200 mg/dL aumenta el riesgo cardiovascular.'
            ),
        },
        'pt': {
            'name': 'Colesterol Total',
            'short_name': 'Colesterol',
            'description': (
                'Soma de todo o colesterol no sangue. '
                'Acima de 200 mg/dL aumenta o risco cardiovascular.'
            ),
        },
    },

    '2085-9': {
        'en': {
            'name': 'HDL Cholesterol',
            'short_name': 'HDL',
            'description': (
                '"Good" cholesterol. Transports cholesterol from arteries to the liver. '
                'High values are protective; low values increase cardiovascular risk.'
            ),
        },
        'es': {
            'name': 'Colesterol HDL',
            'short_name': 'HDL',
            'description': (
                'Colesterol "bueno". Transporta el colesterol de las arterias al hígado. '
                'Valores altos son protectores; valores bajos aumentan el riesgo cardiovascular.'
            ),
        },
        'pt': {
            'name': 'Colesterol HDL',
            'short_name': 'HDL',
            'description': (
                'Colesterol "bom". Transporta o colesterol das artérias para o fígado. '
                'Valores altos são protetores; valores baixos aumentam o risco cardiovascular.'
            ),
        },
    },

    '2089-1': {
        'en': {
            'name': 'LDL Cholesterol',
            'short_name': 'LDL',
            'description': (
                '"Bad" cholesterol. Deposits in arteries promoting atherosclerosis. '
                'The goal is to keep it as low as possible.'
            ),
        },
        'es': {
            'name': 'Colesterol LDL',
            'short_name': 'LDL',
            'description': (
                'Colesterol "malo". Se deposita en las arterias favoreciendo la aterosclerosis. '
                'El objetivo es mantenerlo lo más bajo posible.'
            ),
        },
        'pt': {
            'name': 'Colesterol LDL',
            'short_name': 'LDL',
            'description': (
                'Colesterol "mau". Deposita-se nas artérias favorecendo a aterosclerose. '
                'O objetivo é mantê-lo o mais baixo possível.'
            ),
        },
    },

    '2571-8': {
        'en': {
            'name': 'Triglycerides',
            'short_name': 'TG',
            'description': (
                'Type of fat in the blood. '
                'Elevated levels are associated with obesity, diabetes, and cardiovascular risk.'
            ),
        },
        'es': {
            'name': 'Triglicéridos',
            'short_name': 'Triglicéridos',
            'description': (
                'Tipo de grasa presente en sangre. '
                'Elevados se asocian a obesidad, diabetes y mayor riesgo cardiovascular.'
            ),
        },
        'pt': {
            'name': 'Triglicerídeos',
            'short_name': 'Triglicerídeos',
            'description': (
                'Tipo de gordura presente no sangue. '
                'Valores elevados associam-se à obesidade, diabetes e maior risco cardiovascular.'
            ),
        },
    },

    'ATHEROGENIC_INDEX': {
        'en': {
            'name': 'Atherogenic Index',
            'short_name': 'AI',
            'description': (
                'Ratio Total Cholesterol / HDL. '
                'Estimates cardiovascular risk: the lower, the better.'
            ),
        },
        'es': {
            'name': 'Índice Aterogénico',
            'short_name': 'IA',
            'description': (
                'Cociente Colesterol Total / HDL. '
                'Estima el riesgo cardiovascular: cuanto más bajo, mejor.'
            ),
        },
        'pt': {
            'name': 'Índice Aterogênico',
            'short_name': 'IA',
            'description': (
                'Razão Colesterol Total / HDL. '
                'Estima o risco cardiovascular: quanto menor, melhor.'
            ),
        },
    },

    # ── TIROIDES ─────────────────────────────────────────────────────────────

    '3016-3': {
        'en': {
            'name': 'TSH',
            'short_name': 'TSH',
            'description': (
                'Thyroid-stimulating hormone — primary screening test for thyroid function. '
                'Low in hyperthyroidism; high in hypothyroidism.'
            ),
        },
        'es': {
            'name': 'TSH',
            'short_name': 'TSH',
            'description': (
                'Hormona estimulante del tiroides. '
                'Baja en hipertiroidismo; alta en hipotiroidismo. '
                'Es el mejor cribado de función tiroidea.'
            ),
        },
        'pt': {
            'name': 'TSH',
            'short_name': 'TSH',
            'description': (
                'Hormônio estimulante da tireoide. '
                'Baixo no hipertireoidismo; alto no hipotireoidismo. '
                'É o melhor rastreio da função tireoidiana.'
            ),
        },
    },

    '3024-7': {
        'en': {
            'name': 'Free T4',
            'short_name': 'fT4',
            'description': (
                'Free thyroxine — the most important active thyroid hormone. '
                'Low in hypothyroidism; high in hyperthyroidism.'
            ),
        },
        'es': {
            'name': 'T4 Libre',
            'short_name': 'T4L',
            'description': (
                'Tiroxina libre, la hormona tiroidea activa más importante. '
                'Baja en hipotiroidismo; alta en hipertiroidismo.'
            ),
        },
        'pt': {
            'name': 'T4 Livre',
            'short_name': 'T4L',
            'description': (
                'Tiroxina livre, o hormônio tireoidiano ativo mais importante. '
                'Baixo no hipotireoidismo; alto no hipertireoidismo.'
            ),
        },
    },

    # ── HIERRO ───────────────────────────────────────────────────────────────

    '2498-4': {
        'en': {
            'name': 'Serum Iron',
            'short_name': 'Fe',
            'description': 'Amount of iron circulating in the blood. Varies throughout the day.',
        },
        'es': {
            'name': 'Hierro Sérico',
            'short_name': 'Hierro',
            'description': 'Cantidad de hierro circulando en la sangre. Varía mucho a lo largo del día.',
        },
        'pt': {
            'name': 'Ferro Sérico',
            'short_name': 'Ferro',
            'description': 'Quantidade de ferro circulando no sangue. Varia muito ao longo do dia.',
        },
    },

    '2276-4': {
        'en': {
            'name': 'Ferritin',
            'short_name': 'Ferritin',
            'description': (
                'Iron-storage protein. '
                'The best indicator of iron reserves. '
                'Low values indicate iron deficiency before anemia appears.'
            ),
        },
        'es': {
            'name': 'Ferritina',
            'short_name': 'Ferritina',
            'description': (
                'Proteína de almacenamiento de hierro. '
                'Es el mejor indicador de las reservas de hierro del organismo. '
                'Valores bajos indican déficit de hierro antes de que aparezca anemia.'
            ),
        },
        'pt': {
            'name': 'Ferritina',
            'short_name': 'Ferritina',
            'description': (
                'Proteína de armazenamento de ferro. '
                'É o melhor indicador das reservas de ferro do organismo. '
                'Valores baixos indicam déficit de ferro antes do aparecimento de anemia.'
            ),
        },
    },

    '3034-6': {
        'en': {
            'name': 'Transferrin',
            'short_name': 'Transf',
            'description': 'Iron transport protein. Increases when there is iron deficiency.',
        },
        'es': {
            'name': 'Transferrina',
            'short_name': 'Transferrina',
            'description': 'Proteína transportadora de hierro. Aumenta cuando hay déficit de hierro.',
        },
        'pt': {
            'name': 'Transferrina',
            'short_name': 'Transferrina',
            'description': 'Proteína transportadora de ferro. Aumenta quando há déficit de ferro.',
        },
    },

    '2502-3': {
        'en': {
            'name': 'Transferrin Saturation',
            'short_name': 'TSAT',
            'description': 'Percentage of transferrin loaded with iron.',
        },
        'es': {
            'name': 'Saturación de Transferrina',
            'short_name': 'Sat. Fe',
            'description': 'Porcentaje de transferrina que está cargada de hierro.',
        },
        'pt': {
            'name': 'Saturação de Transferrina',
            'short_name': 'Sat. Fe',
            'description': 'Percentagem de transferrina carregada de ferro.',
        },
    },

    '2500-7': {
        'en': {
            'name': 'TIBC',
            'short_name': 'TIBC',
            'description': 'Total iron-binding capacity. Increases in iron deficiency.',
        },
        'es': {
            'name': 'TIBC',
            'short_name': 'TIBC',
            'description': 'Capacidad total de fijación del hierro. Aumenta en deficiencia de hierro.',
        },
        'pt': {
            'name': 'TIBC',
            'short_name': 'TIBC',
            'description': 'Capacidade total de ligação ao ferro. Aumenta na deficiência de ferro.',
        },
    },

    # ── INFLAMACIÓN ──────────────────────────────────────────────────────────

    '1988-5': {
        'en': {
            'name': 'C-Reactive Protein',
            'short_name': 'CRP',
            'description': (
                'Acute-phase inflammation marker. '
                'Rises rapidly in response to infection, trauma, or systemic inflammation.'
            ),
        },
        'es': {
            'name': 'Proteína C Reactiva',
            'short_name': 'PCR',
            'description': (
                'Marcador de inflamación aguda. '
                'Se eleva rápidamente ante infecciones, traumatismos o inflamación sistémica.'
            ),
        },
        'pt': {
            'name': 'Proteína C Reativa',
            'short_name': 'PCR',
            'description': (
                'Marcador de inflamação aguda. '
                'Eleva-se rapidamente em infecções, traumatismos ou inflamação sistémica.'
            ),
        },
    },

    '4537-7': {
        'en': {
            'name': 'Erythrocyte Sedimentation Rate',
            'short_name': 'ESR',
            'description': (
                'Rate at which red blood cells settle in one hour. '
                'Non-specific indicator of chronic inflammation.'
            ),
        },
        'es': {
            'name': 'Velocidad de Sedimentación Globular',
            'short_name': 'VSG',
            'description': (
                'Velocidad a la que los glóbulos rojos se sedimentan en una hora. '
                'Indicador inespecífico de inflamación crónica.'
            ),
        },
        'pt': {
            'name': 'Velocidade de Hemossedimentação',
            'short_name': 'VHS',
            'description': (
                'Velocidade com que os glóbulos vermelhos sedimentam em uma hora. '
                'Indicador inespecífico de inflamação crónica.'
            ),
        },
    },

    '3255-7': {
        'en': {
            'name': 'Fibrinogen',
            'short_name': 'Fibr',
            'description': (
                'Coagulation protein and acute-phase reactant. '
                'Elevated in chronic inflammation and a cardiovascular risk factor.'
            ),
        },
        'es': {
            'name': 'Fibrinógeno',
            'short_name': 'Fibrinógeno',
            'description': (
                'Proteína de la coagulación y reactante de fase aguda. '
                'Elevado en inflamación crónica y factor de riesgo cardiovascular.'
            ),
        },
        'pt': {
            'name': 'Fibrinogênio',
            'short_name': 'Fibrinogênio',
            'description': (
                'Proteína da coagulação e reagente de fase aguda. '
                'Elevado na inflamação crónica e fator de risco cardiovascular.'
            ),
        },
    },

    # ── ORINA ────────────────────────────────────────────────────────────────

    '2756-5': {
        'en': {
            'name': 'Urine pH',
            'short_name': 'pH',
            'description': 'Acidity of urine. Varies with diet and hydration status.',
        },
        'es': {
            'name': 'pH Urinario',
            'short_name': 'pH orina',
            'description': 'Acidez de la orina. Varía con la dieta y el estado de hidratación.',
        },
        'pt': {
            'name': 'pH Urinário',
            'short_name': 'pH urina',
            'description': 'Acidez da urina. Varia com a dieta e o estado de hidratação.',
        },
    },

    '5811-5': {
        'en': {
            'name': 'Urine Specific Gravity',
            'short_name': 'SG',
            'description': "Indicates the kidney's ability to concentrate urine.",
        },
        'es': {
            'name': 'Densidad Urinaria',
            'short_name': 'Densidad orina',
            'description': 'Indica la capacidad del riñón para concentrar la orina.',
        },
        'pt': {
            'name': 'Densidade Urinária',
            'short_name': 'Densidade urina',
            'description': 'Indica a capacidade do rim de concentrar a urina.',
        },
    },

    '2349-9': {
        'en': {
            'name': 'Urine Glucose',
            'short_name': 'Glu-U',
            'description': 'Glucose in urine. Appears when blood glucose exceeds the renal threshold (~180 mg/dL).',
        },
        'es': {
            'name': 'Glucosa en Orina',
            'short_name': 'Glucosuria',
            'description': 'Glucosa en orina. Aparece cuando la glucemia supera el umbral renal (~180 mg/dL).',
        },
        'pt': {
            'name': 'Glicose na Urina',
            'short_name': 'Glicosúria',
            'description': 'Glicose na urina. Aparece quando a glicemia supera o limiar renal (~180 mg/dL).',
        },
    },

    '2888-6': {
        'en': {
            'name': 'Urine Protein',
            'short_name': 'Prot-U',
            'description': (
                'Proteins in urine. Persistent presence (proteinuria) may indicate '
                'kidney damage or hypertension.'
            ),
        },
        'es': {
            'name': 'Proteínas en Orina',
            'short_name': 'Proteinuria',
            'description': (
                'Proteínas en orina. Su presencia persistente (proteinuria) puede indicar '
                'daño renal o hipertensión.'
            ),
        },
        'pt': {
            'name': 'Proteínas na Urina',
            'short_name': 'Proteinúria',
            'description': (
                'Proteínas na urina. A presença persistente (proteinúria) pode indicar '
                'dano renal ou hipertensão.'
            ),
        },
    },

    '5821-4': {
        'en': {
            'name': 'Urine Leukocytes',
            'short_name': 'WBC-U',
            'description': 'Leukocytes in urine sediment. Elevated values suggest urinary tract infection.',
        },
        'es': {
            'name': 'Leucocitos en Orina',
            'short_name': 'Leu. orina',
            'description': 'Leucocitos en sedimento urinario. Elevados sugieren infección urinaria.',
        },
        'pt': {
            'name': 'Leucócitos na Urina',
            'short_name': 'Leu. urina',
            'description': 'Leucócitos no sedimento urinário. Valores elevados sugerem infecção urinária.',
        },
    },

    '13945-1': {
        'en': {
            'name': 'Urine Red Blood Cells',
            'short_name': 'RBC-U',
            'description': 'Red blood cells in urine. More than 3/field may indicate lithiasis, infection, or renal pathology.',
        },
        'es': {
            'name': 'Hematíes en Orina',
            'short_name': 'Hematuria',
            'description': 'Glóbulos rojos en orina. Más de 3/campo puede indicar litiasis, infección o patología renal.',
        },
        'pt': {
            'name': 'Hemácias na Urina',
            'short_name': 'Hematúria',
            'description': 'Glóbulos vermelhos na urina. Mais de 3/campo pode indicar litíase, infecção ou patologia renal.',
        },
    },

    '2514-8': {
        'en': {
            'name': 'Urine Ketones',
            'short_name': 'Ket-U',
            'description': 'Ketones in urine. Appear in prolonged fasting, ketogenic diets, or diabetic ketoacidosis.',
        },
        'es': {
            'name': 'Cuerpos Cetónicos en Orina',
            'short_name': 'Cetonuria',
            'description': 'Cetonas en orina. Aparecen en ayuno prolongado, dietas cetogénicas o cetoacidosis diabética.',
        },
        'pt': {
            'name': 'Corpos Cetônicos na Urina',
            'short_name': 'Cetonúria',
            'description': 'Cetonas na urina. Aparecem em jejum prolongado, dietas cetogênicas ou cetoacidose diabética.',
        },
    },

    # ── VITAMINAS ────────────────────────────────────────────────────────────

    '1989-3': {
        'en': {
            'name': 'Vitamin D (25-OH)',
            'short_name': 'Vit D',
            'description': (
                'The sunshine vitamin. Essential for calcium absorption, immune function, and bone health. '
                'Deficiency is very common (< 20 ng/mL).'
            ),
        },
        'es': {
            'name': 'Vitamina D (25-OH)',
            'short_name': 'Vit. D',
            'description': (
                'La vitamina del sol. Esencial para la absorción de calcio, '
                'la función inmune y la salud ósea. '
                'Deficiencia muy frecuente (< 20 ng/mL).'
            ),
        },
        'pt': {
            'name': 'Vitamina D (25-OH)',
            'short_name': 'Vit. D',
            'description': (
                'A vitamina do sol. Essencial para a absorção de cálcio, '
                'a função imune e a saúde óssea. '
                'Deficiência muito frequente (< 20 ng/mL).'
            ),
        },
    },

    '2132-9': {
        'en': {
            'name': 'Vitamin B12',
            'short_name': 'B12',
            'description': (
                'Essential for red blood cell formation and the nervous system. '
                'Deficiency causes megaloblastic anemia and neuropathy. '
                'At risk: vegans and the elderly.'
            ),
        },
        'es': {
            'name': 'Vitamina B12',
            'short_name': 'B12',
            'description': (
                'Esencial para la formación de glóbulos rojos y el sistema nervioso. '
                'Su déficit causa anemia megaloblástica y neuropatía. '
                'Riesgo en veganos y personas mayores.'
            ),
        },
        'pt': {
            'name': 'Vitamina B12',
            'short_name': 'B12',
            'description': (
                'Essencial para a formação de glóbulos vermelhos e o sistema nervoso. '
                'A deficiência causa anemia megaloblástica e neuropatia. '
                'Risco em veganos e idosos.'
            ),
        },
    },

    '2284-8': {
        'en': {
            'name': 'Folic Acid',
            'short_name': 'Folate',
            'description': (
                'Vitamin B9. Fundamental for DNA synthesis and red blood cell formation. '
                'Critical during pregnancy to prevent neural tube defects.'
            ),
        },
        'es': {
            'name': 'Ácido Fólico',
            'short_name': 'Folato',
            'description': (
                'Vitamina B9. Fundamental para la síntesis de ADN y la formación de glóbulos rojos. '
                'Crítico en el embarazo para prevenir defectos del tubo neural.'
            ),
        },
        'pt': {
            'name': 'Ácido Fólico',
            'short_name': 'Folato',
            'description': (
                'Vitamina B9. Fundamental para a síntese de ADN e a formação de glóbulos vermelhos. '
                'Crítico na gravidez para prevenir defeitos do tubo neural.'
            ),
        },
    },

    # ── OTRO ─────────────────────────────────────────────────────────────────

    '2857-1': {
        'en': {
            'name': 'Total PSA',
            'short_name': 'PSA',
            'description': (
                'Prostate-specific antigen (men only). '
                'Used for prostate cancer screening. '
                'May also be elevated in benign prostatic hyperplasia or prostatitis.'
            ),
        },
        'es': {
            'name': 'PSA Total',
            'short_name': 'PSA',
            'description': (
                'Antígeno prostático específico (solo hombres). '
                'Se usa para el cribado de cáncer de próstata. '
                'Puede elevarse también por hiperplasia benigna o prostatitis.'
            ),
        },
        'pt': {
            'name': 'PSA Total',
            'short_name': 'PSA',
            'description': (
                'Antígeno prostático específico (apenas homens). '
                'Usado para rastreio do câncer de próstata. '
                'Pode elevar-se também em hiperplasia benigna ou prostatite.'
            ),
        },
    },

    '17861-6': {
        'en': {
            'name': 'Calcium',
            'short_name': 'Ca',
            'description': (
                'Essential mineral for bones, teeth, nerves, and muscles. '
                'Hypocalcemia and hypercalcemia have serious consequences.'
            ),
        },
        'es': {
            'name': 'Calcio',
            'short_name': 'Calcio',
            'description': (
                'Mineral esencial para huesos, dientes, nervios y músculos. '
                'Hipocalcemia e hipercalcemia tienen consecuencias serias.'
            ),
        },
        'pt': {
            'name': 'Cálcio',
            'short_name': 'Cálcio',
            'description': (
                'Mineral essencial para ossos, dentes, nervos e músculos. '
                'Hipocalcemia e hipercalcemia têm consequências graves.'
            ),
        },
    },

    '2777-1': {
        'en': {
            'name': 'Phosphorus',
            'short_name': 'P',
            'description': 'Works together with calcium in bone and muscle health.',
        },
        'es': {
            'name': 'Fósforo',
            'short_name': 'Fósforo',
            'description': 'Trabaja junto al calcio en la salud ósea y muscular.',
        },
        'pt': {
            'name': 'Fósforo',
            'short_name': 'Fósforo',
            'description': 'Trabalha junto ao cálcio na saúde óssea e muscular.',
        },
    },

    '2951-2': {
        'en': {
            'name': 'Sodium',
            'short_name': 'Na',
            'description': (
                'Main electrolyte of extracellular fluid. '
                'Regulates fluid balance and blood pressure.'
            ),
        },
        'es': {
            'name': 'Sodio',
            'short_name': 'Na',
            'description': (
                'Electrolito principal del líquido extracelular. '
                'Regula el equilibrio hídrico y la tensión arterial.'
            ),
        },
        'pt': {
            'name': 'Sódio',
            'short_name': 'Na',
            'description': (
                'Principal eletrólito do líquido extracelular. '
                'Regula o equilíbrio hídrico e a pressão arterial.'
            ),
        },
    },

    '2823-3': {
        'en': {
            'name': 'Potassium',
            'short_name': 'K',
            'description': (
                'Key electrolyte for cardiac and muscular function. '
                'Hypokalemia and hyperkalemia can cause arrhythmias.'
            ),
        },
        'es': {
            'name': 'Potasio',
            'short_name': 'K',
            'description': (
                'Electrolito clave en la función cardíaca y muscular. '
                'Hipopotasemia e hiperpotasemia pueden causar arritmias.'
            ),
        },
        'pt': {
            'name': 'Potássio',
            'short_name': 'K',
            'description': (
                'Eletrólito chave na função cardíaca e muscular. '
                'Hipopotassemia e hiperpotassemia podem causar arritmias.'
            ),
        },
    },

    '2075-0': {
        'en': {
            'name': 'Chloride',
            'short_name': 'Cl',
            'description': 'Electrolyte that maintains acid-base balance and plasma osmolarity.',
        },
        'es': {
            'name': 'Cloro',
            'short_name': 'Cl',
            'description': 'Electrolito que mantiene el equilibrio ácido-base y la osmolaridad plasmática.',
        },
        'pt': {
            'name': 'Cloreto',
            'short_name': 'Cl',
            'description': 'Eletrólito que mantém o equilíbrio ácido-base e a osmolaridade plasmática.',
        },
    },
}


# ---------------------------------------------------------------------------
# API pública
# ---------------------------------------------------------------------------

def _resolve_lang():
    """Devuelve el código de idioma de 2 letras del idioma activo."""
    lang = get_language() or 'en'
    return lang[:2].lower()


def get_biomarker_field(loinc_code: str, field: str) -> str:
    """
    Devuelve el campo traducido (name, short_name, description) para el
    LOINC code e idioma activos. Cae en inglés si no hay traducción,
    y devuelve el propio loinc_code si no existe la entrada.
    """
    entry = _T.get(loinc_code, {})
    if not entry:
        return loinc_code if field == 'name' else ''
    lang = _resolve_lang()
    lang_data = entry.get(lang) or entry.get('en') or {}
    return lang_data.get(field, '')
