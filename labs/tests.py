"""Tests de humo para las vistas de LabLocal."""
import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

from labs.models import AnalysisReport, Biomarker, BiomarkerResult, UserProfile


@pytest.fixture
def usuario(db):
    user = User.objects.create_user(username='testuser', password='testpass123')
    UserProfile.objects.update_or_create(user=user, defaults={'biological_sex': 'M'})
    return user


@pytest.fixture
def client_autenticado(usuario):
    client = Client()
    client.login(username='testuser', password='testpass123')
    return client


@pytest.fixture
def biomarcador(db):
    return Biomarker.objects.create(
        name='Glucosa', short_name='GLU', category='BIOQUIMICA', unit='mg/dL',
        ref_min_male=70, ref_max_male=100, ref_min_female=70, ref_max_female=100,
    )


@pytest.fixture
def analitica(usuario, db):
    return AnalysisReport.objects.create(
        user=usuario, name='Reconocimiento 2026', date='2026-01-15', lab_name='Clínica Test'
    )


# ── Smoke tests de vistas ──────────────────────────────────────────────────────

def test_login_get(client):
    resp = client.get(reverse('login'))
    assert resp.status_code == 200


def test_redirige_al_login_si_no_autenticado(client):
    resp = client.get(reverse('dashboard'))
    assert resp.status_code == 302
    assert '/login/' in resp['Location']


def test_dashboard(client_autenticado):
    resp = client_autenticado.get(reverse('dashboard'))
    assert resp.status_code == 200


def test_lista_analiticas(client_autenticado):
    resp = client_autenticado.get(reverse('report_list'))
    assert resp.status_code == 200


def test_crear_analitica_get(client_autenticado):
    resp = client_autenticado.get(reverse('report_create'))
    assert resp.status_code == 200


def test_detalle_analitica(client_autenticado, analitica):
    resp = client_autenticado.get(reverse('report_detail', args=[analitica.pk]))
    assert resp.status_code == 200


def test_editar_analitica_get(client_autenticado, analitica):
    resp = client_autenticado.get(reverse('report_update', args=[analitica.pk]))
    assert resp.status_code == 200


def test_eliminar_analitica_get(client_autenticado, analitica):
    resp = client_autenticado.get(reverse('report_delete', args=[analitica.pk]))
    assert resp.status_code == 200


def test_lista_biomarcadores(client_autenticado):
    resp = client_autenticado.get(reverse('biomarker_list'))
    assert resp.status_code == 200


def test_detalle_biomarcador(client_autenticado, biomarcador):
    resp = client_autenticado.get(reverse('biomarker_detail', args=[biomarcador.pk]))
    assert resp.status_code == 200


def test_perfil(client_autenticado):
    resp = client_autenticado.get(reverse('profile'))
    assert resp.status_code == 200


def test_exportar(client_autenticado):
    resp = client_autenticado.get(reverse('export'))
    assert resp.status_code == 200
    assert resp['Content-Type'].startswith('application/json')


# ── Tests de lógica de semáforo ────────────────────────────────────────────────

def test_status_normal(usuario, analitica, biomarcador):
    result = BiomarkerResult.objects.create(report=analitica, biomarker=biomarcador, value=85)
    assert result.status == 'normal'


def test_status_alto(usuario, analitica, biomarcador):
    result = BiomarkerResult.objects.create(report=analitica, biomarker=biomarcador, value=120)
    assert result.status == 'high'


def test_status_bajo(usuario, analitica, biomarcador):
    result = BiomarkerResult.objects.create(report=analitica, biomarker=biomarcador, value=50)
    assert result.status == 'low'


def test_status_borderline_alto(usuario, analitica, biomarcador):
    # 100 es el máximo; 110 es 10% sobre el rango (100-70=30), 10/30 ≈ 0.33 → fuera, no límite
    # Límite sería hasta 100 + 30*0.15 = 104.5
    result = BiomarkerResult.objects.create(report=analitica, biomarker=biomarcador, value=103)
    assert result.status == 'borderline'


def test_status_unknown_sin_rango(usuario, analitica, db):
    bm_sin_rango = Biomarker.objects.create(
        name='Prueba', short_name='PRB', category='OTRO', unit='U'
    )
    result = BiomarkerResult.objects.create(report=analitica, biomarker=bm_sin_rango, value=5)
    assert result.status == 'unknown'


def test_crear_analitica_post(client_autenticado, biomarcador):
    data = {
        'name': 'Test analítica',
        'date': '2026-03-01',
        'lab_name': 'Lab Test',
        'notes': '',
        f'biomarker_{biomarcador.pk}_value': '85',
    }
    resp = client_autenticado.post(reverse('report_create'), data)
    assert resp.status_code == 302
    assert AnalysisReport.objects.filter(name='Test analítica').exists()
    assert BiomarkerResult.objects.filter(value=85).exists()
