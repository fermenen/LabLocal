"""
Algoritmo de análisis de frecuencia cardíaca en reposo.

Basado en:
- Curva en U (Clinical Research in Cardiology, 2021): asociación entre FC
  en reposo y mortalidad con 60 lpm como referencia.
- Meta-análisis 46 estudios, 1.246.203 participantes (PMC 2016): cada +10 lpm
  se asocia con +9% de mortalidad por todas las causas.
- Framingham Heart Study / Paris Prospective Study: +10 lpm en 5 años → HR 1.13-1.20.
- AHA: aumento sostenido a lo largo de décadas → +65% riesgo insuficiencia cardíaca.
"""


def heart_rate_scale(bpm):
    """
    Devuelve el estado de la frecuencia cardíaca según evidencia científica.

    Escala basada en curva en U (no rango plano 60-100):
    la zona óptima de menor mortalidad cardiovascular está en 60-70 lpm.
    """
    if bpm is None:
        return {'status': 'unknown'}

    if bpm < 40:
        return {
            'status': 'critical_low',
            'label': 'Bradicardia severa',
            'color': 'red',
            'texto': 'Frecuencia muy baja. Consulta con tu médico.',
        }
    elif bpm < 50:
        return {
            'status': 'low',
            'label': 'Bradicardia leve',
            'color': 'yellow',
            'texto': 'Puede ser normal en personas muy activas físicamente.',
        }
    elif bpm <= 60:
        return {
            'status': 'athlete',
            'label': 'Excelente',
            'color': 'green',
            'texto': 'Asociada a alta forma cardiovascular.',
        }
    elif bpm <= 70:
        return {
            'status': 'optimal',
            'label': 'Óptimo',
            'color': 'green',
            'texto': 'Zona con menor mortalidad cardiovascular demostrada en estudios poblacionales.',
        }
    elif bpm <= 80:
        return {
            'status': 'good',
            'label': 'Normal',
            'color': 'green_light',
            'texto': 'Dentro del rango saludable.',
        }
    elif bpm <= 90:
        return {
            'status': 'elevated',
            'label': 'Ligeramente elevada',
            'color': 'orange',
            'texto': 'El riesgo cardiovascular empieza a subir en este rango.',
        }
    elif bpm <= 100:
        return {
            'status': 'high',
            'label': 'Elevada',
            'color': 'red',
            'texto': 'Asociada a +60% de riesgo de mortalidad vs zona óptima (60-70 lpm).',
        }
    else:
        return {
            'status': 'tachycardia',
            'label': 'Taquicardia',
            'color': 'red',
            'texto': 'Por encima de 100 lpm en reposo. Consulta con tu médico.',
        }


def heart_rate_trend(registros):
    """
    Analiza la tendencia de la frecuencia cardíaca a lo largo del tiempo.

    Requiere mínimo 2 registros con heart_rate definido.
    Basado en Framingham Heart Study: cada +10 lpm en 5 años → +13-20% mortalidad.
    """
    valores = [(r.date, r.heart_rate) for r in registros if r.heart_rate is not None]

    if len(valores) < 2:
        return {'disponible': False}

    fecha_inicio, bpm_inicio = valores[-1]
    fecha_fin, bpm_fin = valores[0]

    años = (fecha_fin - fecha_inicio).days / 365.25
    if años <= 0:
        return {'disponible': False}

    cambio_total = bpm_fin - bpm_inicio
    cambio_anual = cambio_total / años

    if cambio_anual <= -2:
        label = 'Bajando ↓'
        color = 'green'
        texto = 'Tu frecuencia cardíaca está mejorando con el tiempo.'
    elif cambio_anual <= 1:
        label = 'Estable →'
        color = 'yellow'
        texto = 'Tu frecuencia cardíaca se mantiene estable.'
    elif cambio_anual <= 3:
        label = 'Subiendo ligeramente ↑'
        color = 'orange'
        texto = 'Ligera tendencia al alza. Vale la pena seguirla.'
    else:
        label = 'Subiendo ↑↑'
        color = 'red'
        texto = (
            f'+{round(cambio_anual, 1)} lpm/año. '
            'Los estudios Framingham asocian este patrón con mayor riesgo cardiovascular.'
        )

    return {
        'disponible': True,
        'cambio_anual': round(cambio_anual, 1),
        'cambio_total': round(cambio_total, 1),
        'periodo_años': round(años, 1),
        'label': label,
        'color': color,
        'texto': texto,
    }


# Escala visual: rango de display 40–120 bpm (80 bpm de ancho)
HR_DISPLAY_MIN = 40
HR_DISPLAY_MAX = 120


def heart_rate_pct(bpm):
    """Convierte bpm a porcentaje 0-100 para la barra visual (rango 40-120)."""
    return round(max(0, min(100, (bpm - HR_DISPLAY_MIN) / (HR_DISPLAY_MAX - HR_DISPLAY_MIN) * 100)), 1)
