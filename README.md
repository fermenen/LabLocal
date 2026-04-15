# LabLocal

**Personal health data tracker — self-hosted, private by design.**  
Tu historial médico personal, en tu propio servidor. Sin nubes, sin terceros.

Track blood tests, body composition, ECGs and more. All data stays on your own machine.  
Analíticas de sangre, composición corporal, ECGs y más. Todos tus datos, solo tuyos.

![License](https://img.shields.io/badge/license-AGPL--3.0-blue)
![Docker](https://img.shields.io/badge/docker-required-blue)

---

## Requirements

- [Docker](https://docs.docker.com/get-docker/) with Compose v2

That's it.

---

## Install

```bash
git clone https://github.com/fermenen/LabLocal.git
cd lablocal
sh install.sh
```

The installer will:
1. Ask for an admin username, password and host
2. Generate a `.env` with a random secret key
3. Build the Docker image and start the service

Then open **http://localhost:6789** and log in.

---

## Update

```bash
git pull
docker compose -f ./backend/docker-compose.yml up -d --build
```

---

## Commands

| Action | Command |
|---|---|
| Start | `docker compose -f ./backend/docker-compose.yml up -d` |
| Stop | `docker compose -f ./backend/docker-compose.yml down` |
| Logs | `docker compose -f ./backend/docker-compose.yml logs -f` |
| Restart | `docker compose -f ./backend/docker-compose.yml restart` |

---

## Configuration

Edit `backend/.env` to change settings:

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key (auto-generated) |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hostnames |

After editing, restart the container for changes to take effect.

---

## Reverse proxy (optional)

To expose LabLocal on a domain with HTTPS, point your reverse proxy (nginx, Caddy, Traefik…) to `localhost:6789` and add your domain to `ALLOWED_HOSTS`.

Example with Caddy:

```
yourdomain.com {
    reverse_proxy localhost:6789
}
```

---

## License

GNU Affero General Public License v3.0 — see [LICENSE](LICENSE).
