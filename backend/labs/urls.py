"""URLs de la app labs."""
from django.urls import path

from . import views

urlpatterns = [
    # Dashboard
    path('health/', views.health_check, name='health_check'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('reports/all/', views.AllReportsView.as_view(), name='reports_all'),

    
    path('phenoage/', views.PhenoAgeHistoryView.as_view(), name='phenoage_history'),

    # Analíticas
    path('analysis/', views.ReportListView.as_view(), name='analysis_list'),
    path('analysis/new/', views.ReportCreateView.as_view(), name='analysis_create'),
    path('analysis/<int:pk>/', views.ReportDetailView.as_view(), name='analysis_detail'),
    path('analysis/<int:pk>/edit/', views.ReportUpdateView.as_view(), name='analysis_update'),
    path('analysis/<int:pk>/delete/', views.ReportDeleteView.as_view(), name='analysis_delete'),

    # Biomarcadores
    path('biomarkers/', views.BiomarkerListView.as_view(), name='biomarker_list'),
    path('biomarkers/<int:pk>/', views.BiomarkerDetailView.as_view(), name='biomarker_detail'),

    # Composición corporal
    path('body/', views.BodyCompositionListView.as_view(), name='body_list'),
    path('body/new/', views.BodyCompositionCreateView.as_view(), name='body_create'),
    path('body/<int:pk>/', views.BodyCompositionDetailView.as_view(), name='body_detail'),
    path('body/<int:pk>/edit/', views.BodyCompositionUpdateView.as_view(), name='body_update'),
    path('body/<int:pk>/delete/', views.BodyCompositionDeleteView.as_view(), name='body_delete'),

    # Electrocardiogramas
    path('ecg/', views.ECGListView.as_view(), name='ecg_list'),
    path('ecg/new/', views.ECGCreateView.as_view(), name='ecg_create'),
    path('ecg/<int:pk>/', views.ECGDetailView.as_view(), name='ecg_detail'),
    path('ecg/<int:pk>/edit/', views.ECGUpdateView.as_view(), name='ecg_update'),
    path('ecg/<int:pk>/delete/', views.ECGDeleteView.as_view(), name='ecg_delete'),

    # Perfil
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/family/new/', views.FamilyUserCreateView.as_view(), name='family_create'),
    path('profile/password/', views.PasswordChangeView.as_view(), name='password_change'),
    path('profile/privacy/', views.PrivacyView.as_view(), name='privacy'),

    # Exportación
    path('export/', views.ExportView.as_view(), name='export'),
]
