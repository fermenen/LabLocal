# LabLocal — Monorepo

Estructura separada backend + mobile apps.

```
lablocal/
├── backend/              ← Django REST API
│   ├── .env
│   ├── .venv/
│   ├── manage.py
│   ├── medivault/        (config Django)
│   ├── labs/             (app principal)
│   ├── docker-compose.yml
│   ├── Dockerfile
│   └── pyproject.toml
│
├── mobile/               ← Capacitor (Webview → Django)
│   ├── capacitor.config.json
│   ├── package.json
│   ├── android/
│   └── ios/
│
└── CLAUDE.md             (project memory)
```

---

## 🚀 Setup rápido

### Backend (Django)
```bash
cd backend
source .venv/bin/activate
pip install -e .
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

### Mobile (Capacitor + WebView)
```bash
cd mobile
npm install
npx cap run android
# o
npx cap run ios
```

### Docker (Backend + Mobile en emulador)
```bash
cd backend
docker compose up --build
```

---

## 📱 Cómo funciona

- **Web (Desktop):** Django templates + Alpine.js → `/`
- **Mobile (Android/iOS):** Capacitor WebView → carga Django en `http://localhost:8000` (dev) o `https://tu-dominio.com` (prod)

---

## 🔧 Actualizar URL de Backend

**Desarrollo (emulador):**
```json
// mobile/capacitor.config.json
{
  "server": {
    "url": "http://10.0.2.2:8000"  // Android desde emulador
  }
}
```

**Producción:**
```json
{
  "server": {
    "url": "https://tu-dominio.com"
  }
}
```

Luego sincroniza:
```bash
cd mobile
npx cap sync
npx cap open android  # o ios

---

## Licencia

- Este proyecto se distribuye bajo la licencia GNU AFFERO GENERAL PUBLIC LICENSE v3.
- Texto completo en el archivo `LICENSE`.
```
