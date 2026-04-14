"""Context processors globales para la app labs."""
from .models import AILicense


def ai_config(request):
    """Expone si la IA está disponible a todos los templates."""
    if not request.user.is_authenticated:
        return {'ai_enabled': False}
    return {'ai_enabled': bool(AILicense.get_active())}
