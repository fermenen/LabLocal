"""Filtros de template personalizados para LabLocal."""
from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Permite acceder a un diccionario con clave dinámica en templates."""
    if dictionary is None:
        return None
    return dictionary.get(key)


@register.filter
def status_badge_class(status):
    """Devuelve las clases CSS del badge según el estado del semáforo."""
    classes = {
        'normal':     'bg-green-100 text-green-800 border-green-200',
        'borderline': 'bg-yellow-100 text-yellow-800 border-yellow-200',
        'low':        'bg-red-100 text-red-800 border-red-200',
        'high':       'bg-red-100 text-red-800 border-red-200',
        'unknown':    'bg-gray-100 text-gray-600 border-gray-200',
    }
    return classes.get(status, 'bg-gray-100 text-gray-600 border-gray-200')


@register.filter
def status_icon(status):
    """Devuelve el emoji del semáforo según el estado."""
    icons = {
        'normal':     '🟢',
        'borderline': '🟡',
        'low':        '🔴',
        'high':       '🔴',
        'unknown':    '⚪',
    }
    return icons.get(status, '⚪')


@register.filter
def status_label(status):
    """Texto legible del estado del semáforo."""
    labels = {
        'normal':     'Normal',
        'borderline': 'Límite',
        'low':        'Bajo',
        'high':       'Alto',
        'unknown':    'Sin rango',
    }
    return labels.get(status, 'Desconocido')
