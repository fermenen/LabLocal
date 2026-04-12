"""URLs raíz de LabLocal."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.views.generic import RedirectView

handler404 = 'labs.views.custom_404'

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='dashboard'), name='root'),
    path('login/', auth_views.LoginView.as_view(template_name='labs/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', include('labs.urls')),
]

# Servir archivos de medios en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
