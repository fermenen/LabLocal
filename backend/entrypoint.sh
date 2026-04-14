#!/bin/sh
set -e

echo "=== LabLocal — Iniciando ==="

# Crear directorio de datos si no existe
mkdir -p /app/data

# Aplicar migraciones
echo "→ Aplicando migraciones..."
python manage.py migrate --noinput

# Cargar catálogo de biomarcadores
echo "→ Cargando catálogo de biomarcadores..."
python manage.py seed_biomarkers

# Recopilar archivos estáticos
echo "→ Recopilando archivos estáticos..."
python manage.py collectstatic --noinput --clear

echo "=== Arrancando servidor ==="
exec gunicorn medivault.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 2 \
  --timeout 120 \
  --access-logfile - \
  --error-logfile -
