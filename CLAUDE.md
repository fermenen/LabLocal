# LabLocal — Project Memory for Claude Code

> Visor de analíticas médicas, self-hosted, open source (MIT).
> Filosofía Home Assistant: el usuario despliega en su infra, los datos médicos nunca salen de su servidor.

---

## 🎯 En una frase

Aplicación Django que permite guardar, visualizar y entender analíticas médicas (reconocimientos laborales, análisis clínicos) en tu propia infraestructura. Sin enviar datos a terceros. Sin suscripciones.

---

## Stack

| Capa | Tecnología |
|---|---|
| Backend | Django 5.1 + SQLite (default) |
| Frontend | Django Templates + Alpine.js (CDN) + Tailwind CSS (CDN Play) |
| Gráficas | Chart.js 4.x (CDN) |
| Auth | Django Auth nativo |
| Despliegue | Docker + docker-compose + gunicorn + whitenoise |

**Reglas de stack (no cambiar en MVP):**
- Sin DRF / API REST — server-side rendered
- Sin Celery — todo síncrono
- Sin Node/npm en producción — Tailwind y Alpine.js por CDN
- SQLite por defecto — PostgreSQL opcional via DATABASE_URL en .env

---

## Estructura del proyecto

```
lablocal/
├── CLAUDE.md                  ← este archivo
├── docker-compose.yml
├── Dockerfile
├── .env.example
├── requirements.txt
├── manage.py
├── medivault/                 ← config Django (settings, urls, wsgi)
└── labs/                      ← app principal
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── forms.py
    ├── admin.py
    ├── fixtures/biomarkers.json
    ├── management/commands/seed_biomarkers.py
    └── templates/labs/
        ├── base.html
        ├── dashboard.html
        ├── report_list.html
        ├── report_form.html
        ├── report_detail.html
        └── biomarker_detail.html
```

---

## Modelos de datos

### UserProfile
Extiende User de Django. Campos: `birth_date`, `biological_sex` ('M'/'F'), `notes`.

### Biomarker (catálogo, pre-cargado por fixture)
`name`, `short_name`, `loinc_code`, `category` (HEMATOLOGIA / BIOQUIMICA / LIPIDOS / TIROIDES / HIERRO / INFLAMACION / ORINA / VITAMINAS / OTRO), `unit`, `description`, `ref_min_male`, `ref_max_male`, `ref_min_female`, `ref_max_female`, `low_is_bad`, `order`.

### AnalysisReport
`user` (FK), `name`, `date`, `lab_name`, `notes`, `created_at`.

### BiomarkerResult
`report` (FK, CASCADE), `biomarker` (FK, PROTECT), `value` (Decimal), `notes`.
Property calculada: `status` → 'normal' | 'low' | 'high' | 'unknown' usando sexo del usuario.

---

## URLs

```
/                    → redirect a /dashboard o /login
/login/              → LoginView
/logout/             → LogoutView
/dashboard/          → resumen, alertas, acceso rápido
/reports/            → lista de analíticas
/reports/new/        → crear analítica (meta + valores)
/reports/<id>/       → detalle analítica con semáforo
/reports/<id>/edit/  → editar
/reports/<id>/delete/→ borrar
/biomarkers/         → catálogo de biomarcadores
/biomarkers/<id>/    → detalle + gráfico histórico
/profile/            → editar perfil
/export/             → descarga JSON de todos los datos
/admin/              → Django Admin
```

---

## Sistema semáforo

Cada `BiomarkerResult` calcula su `status`:
- 🟢 **NORMAL** — dentro del rango ref del sexo del usuario
- 🟡 **LÍMITE** — entre 0% y 15% fuera del rango (borderline)
- 🔴 **FUERA** — más de 15% fuera del rango
- ⚪ **SIN RANGO** — no hay referencia definida

---

## Design tokens (CSS vars en base.html)

```css
--color-brand:  #2B5EA7   /* azul médico — nav, headings, botones */
--color-accent: #1A9E6E   /* verde — normal/OK */
--color-warn:   #D97706   /* ámbar — límite/atención */
--color-danger: #DC2626   /* rojo — fuera de rango */
--color-bg:     #F8FAFC
--color-card:   #FFFFFF
--color-text:   #1A2340
--color-muted:  #64748B
```

---

## Convenciones de código

- **Views**: Class-Based Views con `LoginRequiredMixin` en todas
- **Forms**: `ModelForm` para formularios de modelo
- **Templates**: heredan de `base.html` con `{% block content %}`
- **JS**: solo Alpine.js directivas en templates; nada de JS inline
- **Docstrings**: en español (proyecto de comunidad hispana)
- **Tests**: al menos smoke test por view (pytest-django)

---

## Comandos frecuentes

```bash
# Dev local
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_biomarkers
python manage.py createsuperuser
python manage.py runserver

# Docker
docker compose up --build
docker compose exec web python manage.py shell
docker compose logs -f web
```

---

## Biomarcadores pre-cargados (~60)

Hematología (13): Leucocitos, Eritrocitos, Hemoglobina, Hematocrito, VCM, HCM, CHCM, Plaquetas, Neutrófilos, Linfocitos, Monocitos, Eosinófilos, Basófilos

Bioquímica (12): Glucosa, HbA1c, Urea, Creatinina, Ácido úrico, Bilirrubina total, Proteínas totales, Albúmina, AST, ALT, GGT, Fosfatasa alcalina

Lípidos (5): Colesterol total, HDL, LDL, Triglicéridos, Índice aterogénico

Tiroides (2): TSH, T4 libre

Hierro (5): Hierro sérico, Ferritina, Transferrina, Saturación transferrina, TIBC

Inflamación (3): PCR, VSG, Fibrinógeno

Orina (7): pH, Densidad, Glucosa, Proteínas, Leucocitos, Hematíes, Cetona

Vitaminas (3): Vitamina D, B12, Ácido fólico

Otros (6+): PSA, Calcio, Fósforo, Sodio, Potasio, Cloro

---

## Hoja de ruta

- **v0.1 (MVP)** — entrada manual, visor, semáforo, gráficas, exportación JSON, Docker ← AHORA
- **v0.2** — importación PDF con OCR (vision LLM / Tesseract)
- **v0.3** — módulo IA: consejos con API key propia (OpenAI / Anthropic / Ollama)
- **v0.4** — multi-usuario / perfiles de familia
- **v0.5** — importación HL7/FHIR
- **v1.0** — PWA, i18n, tema oscuro

---

## Decisiones tomadas (no reabrir sin actualizar este doc)

1. SQLite por defecto, sin cambiar a Postgres sin DATABASE_URL en .env
2. Sin API REST en MVP — todo server-side rendered
3. Sin Celery ni async en MVP
4. Sin multitenancy en MVP
5. Tailwind y Alpine.js por CDN — sin build step
6. Posicionamiento como herramienta educativa, NO diagnóstica (evitar EU MDR Class IIa)

---

## Referencias clave

- Rangos de referencia: ARUP Laboratories, ABIM Lab Reference Ranges
- Codificación: LOINC (loinc.org)
- Regulación España: Ley 31/1995 PRL art. 22
- Inspiración: Home Assistant (homeassistant.io), Ornament Health
