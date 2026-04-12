"""
Cálculo de Edad Fenotípica (PhenoAge) según Levine et al. 2018.

Referencia:
  Levine ME et al. "An epigenetic biomarker of aging for lifespan and healthspan."
  Aging (Albany NY). 2018;10(4):573-591. doi:10.18632/aging.101414

El algoritmo usa un modelo Gompertz proporcional ajustado en NHANES III
con 9 biomarcadores de analítica estándar más la edad cronológica.

Unidades de entrada requeridas:
  age            años
  albumin        g/dL
  creatinine     mg/dL
  glucose        mg/dL  (se convierte internamente a mmol/L)
  crp_mgl        mg/L   (se convierte internamente a mg/dL para ln)
  lymph_pct      %      (derivado de LYMPH/WBC × 100)
  mcv            fL
  rdw            %
  alp            U/L
  wbc            10³/μL
"""

import math
from decimal import Decimal

# ── Coeficientes del modelo (Tabla S2 del paper) ──────────────────────────────
_COEF = {
    'intercept':  -19.9067,
    'age':          0.0804,
    'albumin':     -0.0336,   # g/dL
    'creatinine':   0.0095,   # mg/dL
    'glucose':      0.1953,   # mmol/L  ← glucosa en mg/dL ÷ 18.016
    'log_crp':      0.0954,   # ln(CRP en mg/dL) ← CRP en mg/L ÷ 10
    'lymph_pct':   -0.0120,   # %
    'mcv':          0.0268,   # fL
    'rdw':          0.3306,   # %
    'alp':          0.00188,  # U/L
    'wbc':          0.0554,   # 10³/μL
}

_LAMBDA = 0.0076927   # parámetro de forma Gompertz (escala mensual)
_T = 120              # horizonte de mortalidad: 120 meses = 10 años


def _mortality_to_phenoage(mortality: float) -> float:
    mortality = min(mortality, 0.9999)
    return 141.50225 + math.log(-0.00553 * math.log(1.0 - mortality)) / 0.09165


def compute_phenoage(*, age, albumin, creatinine, glucose_mgdl,
                     crp_mgl, lymph_pct, mcv, rdw, alp, wbc) -> float:
    """Calcula la edad fenotípica (PhenoAge) en años."""
    glucose_mmol = glucose_mgdl / 18.016
    crp_mgdl = max(crp_mgl / 10.0, 0.001)  # evitar log(0)

    xb = (
        _COEF['intercept']
        + _COEF['age']       * age
        + _COEF['albumin']   * albumin
        + _COEF['creatinine']* creatinine
        + _COEF['glucose']   * glucose_mmol
        + _COEF['log_crp']   * math.log(crp_mgdl)
        + _COEF['lymph_pct'] * lymph_pct
        + _COEF['mcv']       * mcv
        + _COEF['rdw']       * rdw
        + _COEF['alp']       * alp
        + _COEF['wbc']       * wbc
    )

    mortality = 1.0 - math.exp(
        -math.exp(xb) * (math.exp(_LAMBDA * _T) - 1.0) / _LAMBDA
    )
    return round(_mortality_to_phenoage(mortality), 1)


# Biomarcadores necesarios: short_name → etiqueta legible
_REQUIRED = {
    'ALB':  'Albúmina',
    'CREA': 'Creatinina',
    'GLU':  'Glucosa',
    'PCR':  'PCR',
    'VCM':  'VCM',
    'RDW':  'RDW',
    'FA':   'Fosfatasa Alcalina',
    'WBC':  'Leucocitos',
    'LYMPH':'Linfocitos',
}


def _split_years_months(years_value):
    total_months = round(abs(float(years_value)) * 12)
    return total_months // 12, total_months % 12


def calculate_report_phenoage(report):
    """Calcula PhenoAge para una analítica usando la edad en la fecha del informe."""
    try:
        birth_date = report.user.userprofile.birth_date
    except Exception:
        return None

    if not birth_date or not report.date:
        return None

    chrono_age = (report.date - birth_date).days / 365.25
    vals = {
        r.biomarker.short_name: float(r.value)
        for r in report.results.select_related('biomarker')
    }
    missing = [label for key, label in _REQUIRED.items() if key not in vals]

    if missing:
        return {
            'phenoage': None,
            'chrono_age': round(chrono_age, 1),
            'diff': None,
            'missing': missing,
        }

    lymph_pct = (vals['LYMPH'] / vals['WBC']) * 100 if vals['WBC'] > 0 else 0
    pheno = compute_phenoage(
        age=chrono_age,
        albumin=vals['ALB'],
        creatinine=vals['CREA'],
        glucose_mgdl=vals['GLU'],
        crp_mgl=vals['PCR'],
        lymph_pct=lymph_pct,
        mcv=vals['VCM'],
        rdw=vals['RDW'],
        alp=vals['FA'],
        wbc=vals['WBC'],
    )
    diff = round(chrono_age - pheno, 1)

    return {
        'phenoage': pheno,
        'chrono_age': round(chrono_age, 1),
        'diff': diff,
        'missing': [],
    }


def update_report_phenoage(report):
    """Persiste PhenoAge en la analítica después de crear o editar resultados."""
    result = calculate_report_phenoage(report)
    if not result:
        report.phenoage_years = None
        report.phenoage_delta_years = None
        report.phenoage_missing = 'Fecha de nacimiento no definida'
    elif result['phenoage'] is None:
        report.phenoage_years = None
        report.phenoage_delta_years = None
        report.phenoage_missing = ', '.join(result['missing'])
    else:
        report.phenoage_years = Decimal(str(result['phenoage']))
        report.phenoage_delta_years = Decimal(str(result['diff']))
        report.phenoage_missing = ''

    report.save(update_fields=['phenoage_years', 'phenoage_delta_years', 'phenoage_missing'])
    return result


def get_phenoage_from_report(report):
    """Devuelve datos listos para la tarjeta de dashboard usando valores persistidos."""
    if not report:
        return None

    if report.phenoage_years is None:
        missing = [m.strip() for m in report.phenoage_missing.split(',') if m.strip()]
        return {
            'phenoage': None,
            'missing': missing,
        }

    pheno = float(report.phenoage_years)
    diff = float(report.phenoage_delta_years or 0)
    pheno_years, pheno_months = _split_years_months(pheno)
    diff_years, diff_months = _split_years_months(diff)
    return {
        'phenoage': pheno,
        'pheno_years': pheno_years,
        'pheno_months': pheno_months,
        'diff': diff,
        'diff_years': diff_years,
        'diff_months': diff_months,
        'younger': diff > 0,
        'missing': [],
    }
