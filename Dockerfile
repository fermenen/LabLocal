FROM python:3.12-slim

# Copiar el binario de uv desde su imagen oficial
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Instalar dependencias (capa cacheada — solo se reconstruye si cambia pyproject.toml/uv.lock)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Copiar código fuente
COPY . .

RUN chmod +x entrypoint.sh && mkdir -p /app/data /app/staticfiles

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
