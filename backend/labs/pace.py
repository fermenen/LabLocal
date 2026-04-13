"""
Aproximación del Pace of Aging a partir de dos analíticas de sangre.

Inspirado en DunedinPACE (Belsky et al., eLife 2020), adaptado para
biomarcadores de analítica estándar disponibles sin test epigenético.

Escala: 1.0 = ritmo promedio de envejecimiento
        < 1.0 = más lento que la media  🟢
        > 1.0 = más rápido que la media 🔴

Referencia:
    Belsky DW et al. "Quantification of the pace of biological aging
    in humans through a blood test." eLife 2020;9:e54870.
"""

# Biomarcadores disponibles en analítica estándar que cambian con el envejecimiento.
# direction='increasing'  → subir = envejecimiento
# direction='decreasing'  → bajar = envejecimiento
_BIOMARKERS = {
    'ALB':  {'direction': 'decreasing'},  # albúmina:          baja con edad (función hepática/renal)
    'CREA': {'direction': 'increasing'},  # creatinina:        sube (función renal)
    'GLU':  {'direction': 'increasing'},  # glucosa:           resistencia insulínica
    'PCR':  {'direction': 'increasing'},  # PCR:               inflamación crónica (inflammaging)
    'HGB':  {'direction': 'decreasing'},  # hemoglobina:       anemia de la edad
    'FA':   {'direction': 'increasing'},  # fosfatasa alcalina: daño óseo/hepático
    'RDW':  {'direction': 'increasing'},  # ancho distribución eritrocitaria: estrés hematopoyético
    'WBC':  {'direction': 'increasing'},  # leucocitos:        inflamación sistémica
}

MIN_BIOMARKERS = 4    # mínimo de biomarcadores coincidentes para calcular
MIN_DAYS       = 180  # mínimo de días entre analíticas (≈ 6 meses)
SCALE_FACTOR   = 10   # empírico: pace = 1 + cambio_medio * SCALE_FACTOR
PACE_MIN       = 0.3
PACE_MAX       = 2.5


def _get_value(report, short_name):
    """Devuelve el valor float de un biomarcador en un report, o None."""
    try:
        result = report.results.get(biomarker__short_name=short_name)
        return float(result.value)
    except Exception:
        return None


def _lymph_pct(report):
    """% linfocitos = LYMPH / WBC × 100 (si ambos disponibles)."""
    lymph = _get_value(report, 'LYMPH')
    wbc   = _get_value(report, 'WBC')
    if lymph is not None and wbc and wbc > 0:
        return lymph / wbc * 100
    return None


def calcular_pace(report_actual, report_anterior):
    """
    Calcula el Pace of Aging aproximado entre dos analíticas.

    Parámetros
    ----------
    report_actual   : AnalysisReport más reciente (con results prefetched)
    report_anterior : AnalysisReport más antiguo  (con results prefetched)

    Devuelve
    --------
    dict con claves:
        disponible      bool
        pace            float  (solo si disponible=True)
        interpretacion  tuple  (texto, color_key)
        biomarkers_usados int
        periodo_meses   int
        razon           str    (solo si disponible=False)
    """
    dias = (report_actual.date - report_anterior.date).days

    if dias < MIN_DAYS:
        return {
            'disponible': False,
            'razon': f'Se necesitan al menos 6 meses entre analíticas ({dias} días disponibles)',
        }

    años = dias / 365.25
    cambios = []

    for short_name, cfg in _BIOMARKERS.items():
        v_act = _get_value(report_actual,   short_name)
        v_ant = _get_value(report_anterior, short_name)
        if v_act is None or v_ant is None or v_ant == 0:
            continue

        cambio_pct      = (v_act - v_ant) / abs(v_ant)
        cambio_anual    = cambio_pct / años

        # Un biomarcador que "sube con la edad" y sube → envejecimiento (+)
        # Uno que "baja con la edad" y baja → también envejecimiento (+)
        if cfg['direction'] == 'decreasing':
            cambio_anual = -cambio_anual

        cambios.append(cambio_anual)

    # Linfocitos % (calculado de LYMPH + WBC)
    lp_act = _lymph_pct(report_actual)
    lp_ant = _lymph_pct(report_anterior)
    if lp_act is not None and lp_ant is not None and lp_ant != 0:
        cambio_anual = -(lp_act - lp_ant) / abs(lp_ant) / años  # decreasing
        cambios.append(cambio_anual)

    if len(cambios) < MIN_BIOMARKERS:
        return {
            'disponible': False,
            'razon': f'Datos insuficientes: {len(cambios)} biomarcadores coincidentes (mínimo {MIN_BIOMARKERS})',
        }

    pace_bruto = sum(cambios) / len(cambios)
    pace = 1.0 + pace_bruto * SCALE_FACTOR
    pace = round(max(PACE_MIN, min(PACE_MAX, pace)), 2)

    return {
        'disponible':       True,
        'pace':             pace,
        'interpretacion':   _interpretar(pace),
        'biomarkers_usados': len(cambios),
        'periodo_meses':    round(dias / 30),
    }


def _interpretar(pace):
    """Devuelve (texto_legible, color_key) para el semáforo del dashboard."""
    if pace < 0.7:
        return ('Envejecimiento muy lento',       'normal')
    if pace < 0.9:
        return ('Por debajo de la media',          'normal')
    if pace < 1.1:
        return ('Ritmo normal',                    'normal')
    if pace < 1.3:
        return ('Algo por encima de la media',     'borderline')
    return     ('Envejecimiento acelerado',        'high')
