#!/bin/sh
set -e

BOLD='\033[1m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
RESET='\033[0m'

echo ""
echo "${BOLD}LabLocal — Installer${RESET}"
echo "─────────────────────────────────────"

# ── Checks ────────────────────────────────────────────────────────────────────

if ! command -v docker >/dev/null 2>&1; then
  echo "${RED}Error:${RESET} Docker is not installed."
  echo "Install it from https://docs.docker.com/get-docker/ and try again."
  exit 1
fi

if ! docker compose version >/dev/null 2>&1; then
  echo "${RED}Error:${RESET} Docker Compose (v2) is required."
  echo "Update Docker Desktop or install the compose plugin."
  exit 1
fi

# ── .env ──────────────────────────────────────────────────────────────────────

ENV_FILE="./backend/.env"

if [ -f "$ENV_FILE" ]; then
  echo "${YELLOW}→ $ENV_FILE already exists, skipping generation.${RESET}"
  ALLOWED_HOSTS=$(grep '^ALLOWED_HOSTS=' "$ENV_FILE" | cut -d'=' -f2-)
  ALLOWED_HOSTS=${ALLOWED_HOSTS:-localhost}
else
  echo "→ Generating $ENV_FILE..."

  # Generate a random SECRET_KEY
  SECRET_KEY=$(LC_ALL=C tr -dc 'A-Za-z0-9!@#$%^&*(-_=+)' </dev/urandom 2>/dev/null | head -c 50 || \
               python3 -c "import secrets,string; print(''.join(secrets.choice(string.ascii_letters+string.digits+'!@#\$%^&*(-_=+)') for _ in range(50)))")

  printf "Enter the host/domain where LabLocal will be accessible [localhost / e.g. 192.168.1.100]: "
  read ALLOWED_HOSTS
  ALLOWED_HOSTS=${ALLOWED_HOSTS:-localhost}

  cat > "$ENV_FILE" <<EOF
SECRET_KEY=${SECRET_KEY}
DEBUG=False
ALLOWED_HOSTS=${ALLOWED_HOSTS}
EOF

  echo "${GREEN}✓ $ENV_FILE created.${RESET}"
fi

# ── Docker build + start ───────────────────────────────────────────────────────

echo "→ Building and starting LabLocal..."
docker compose -f ./backend/docker-compose.yml up -d --build

echo ""
echo "→ Waiting for the container to be ready..."
sleep 5

echo "→ Creating admin user..."
docker compose -f ./backend/docker-compose.yml exec web python manage.py createsuperuser

echo ""
HOST=$(echo "$ALLOWED_HOSTS" | cut -d',' -f1)

echo "${GREEN}${BOLD}✓ LabLocal is running!${RESET}"
echo ""
echo "  Open:  http://${HOST}:6789"
echo ""
echo "  Stop:  docker compose -f ./backend/docker-compose.yml down"
echo "  Logs:  docker compose -f ./backend/docker-compose.yml logs -f"
echo ""
