# ─── LabLocal — Makefile ──────────────────────────────────────────────────────
# Requiere: uv (https://docs.astral.sh/uv/)
# Uso: make <target>

.DEFAULT_GOAL := help
.PHONY: help install dev shell migrate migrations seed superuser test lint \
        collectstatic docker-up docker-down docker-build docker-logs docker-shell clean

# ── Colores ───────────────────────────────────────────────────────────────────
CYAN  := \033[0;36m
RESET := \033[0m

# ── Entorno ───────────────────────────────────────────────────────────────────
UV    := uv run
MANAGE := $(UV) python manage.py

# ─────────────────────────────────────────────────────────────────────────────

help: ## Muestra esta ayuda
	@echo ""
	@echo "  LabLocal — comandos disponibles"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  $(CYAN)%-20s$(RESET) %s\n", $$1, $$2}'
	@echo ""

# ── Dependencias ──────────────────────────────────────────────────────────────

install: ## Instala todas las dependencias (prod + dev) con uv
	uv sync

install-prod: ## Instala solo dependencias de producción
	uv sync --no-dev

# ── Desarrollo ────────────────────────────────────────────────────────────────

dev: ## Arranca el servidor de desarrollo en http://0.0.0.0:8000
	$(MANAGE) runserver 0.0.0.0:8000

shell: ## Abre el shell interactivo de Django
	$(MANAGE) shell

# ── Base de datos ─────────────────────────────────────────────────────────────

migrate: ## Aplica las migraciones pendientes
	$(MANAGE) migrate

migrations: ## Genera nuevas migraciones (makemigrations)
	$(MANAGE) makemigrations

seed: ## Carga el catálogo de biomarcadores (~60 marcadores)
	$(MANAGE) seed_biomarkers

demo: ## Carga datos de demostración (analíticas con valores buenos y malos) para admin
	$(MANAGE) seed_demo_data

superuser: ## Crea un superusuario de forma interactiva
	$(MANAGE) createsuperuser

setup: migrate seed superuser ## Bootstrap completo: migrar + seed + superusuario

# ── Tests ─────────────────────────────────────────────────────────────────────

test: ## Ejecuta la suite de tests con pytest
	$(UV) pytest

test-v: ## Tests con salida verbose y sin captura de stdout
	$(UV) pytest -v -s

# ── Estáticos ─────────────────────────────────────────────────────────────────

collectstatic: ## Recopila archivos estáticos para producción
	$(MANAGE) collectstatic --noinput --clear

# ── Docker ────────────────────────────────────────────────────────────────────

docker-build: ## Construye la imagen Docker
	docker compose build

docker-up: ## Arranca los servicios con Docker Compose (rebuild)
	docker compose up --build

docker-up-d: ## Arranca los servicios en segundo plano
	docker compose up --build -d

docker-down: ## Para y elimina los contenedores
	docker compose down

docker-logs: ## Muestra los logs en tiempo real
	docker compose logs -f web

docker-shell: ## Abre un shell dentro del contenedor web
	docker compose exec web python manage.py shell

# ── Limpieza ──────────────────────────────────────────────────────────────────

clean: ## Elimina cachés de Python y archivos temporales
	find . -type d -name __pycache__ -not -path './.venv/*' | xargs rm -rf
	find . -type f -name '*.pyc' -not -path './.venv/*' -delete
	rm -rf .pytest_cache htmlcov .coverage
