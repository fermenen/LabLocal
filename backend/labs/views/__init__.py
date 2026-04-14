"""Paquete de vistas de LabLocal."""
from .core import LoginView, LogoutView, custom_404, health_check
from .dashboard import DashboardView
from .analysis import (
    ReportListView,
    ReportCreateView,
    ReportDetailView,
    ReportUpdateView,
    ReportDeleteView,
    PhenoAgeHistoryView,
)
from .biomarkers import BiomarkerListView, BiomarkerDetailView
from .body import (
    BodyCompositionListView,
    BodyCompositionCreateView,
    BodyCompositionDetailView,
    BodyCompositionUpdateView,
    BodyCompositionDeleteView,
)
from .ecg import (
    ECGListView,
    ECGCreateView,
    ECGDetailView,
    ECGUpdateView,
    ECGDeleteView,
)
from .profile import (
    ProfileView, FamilyUserCreateView, PrivacyView, LanguageView, LanguageChangeView,
    PasswordChangeView, AISubscribeView, AIUnsubscribeView,
)
from .ai_proxy import ConversationsView, MessagesView
from .reports import AllReportsView, ExportView

__all__ = [
    'LoginView', 'LogoutView', 'custom_404', 'health_check',
    'DashboardView',
    'ReportListView', 'ReportCreateView', 'ReportDetailView',
    'ReportUpdateView', 'ReportDeleteView', 'PhenoAgeHistoryView',
    'BiomarkerListView', 'BiomarkerDetailView',
    'BodyCompositionListView', 'BodyCompositionCreateView', 'BodyCompositionDetailView',
    'BodyCompositionUpdateView', 'BodyCompositionDeleteView',
    'ECGListView', 'ECGCreateView', 'ECGDetailView', 'ECGUpdateView', 'ECGDeleteView',
    'ProfileView', 'FamilyUserCreateView', 'PrivacyView', 'LanguageView', 'LanguageChangeView', 'PasswordChangeView', 'AISubscribeView', 'AIUnsubscribeView',
    'ConversationsView', 'MessagesView',
    'AllReportsView', 'ExportView',
]
