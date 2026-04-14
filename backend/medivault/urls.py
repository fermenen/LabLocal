"""URLs raíz de LabLocal."""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.views.generic import RedirectView

from labs.views import LoginView, LogoutView

handler404 = 'labs.views.custom_404'

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='dashboard'), name='root'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include('labs.urls')),
]

# Servir archivos de medios (Django los sirve directamente al no haber nginx delante)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
