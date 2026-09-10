# HouseMe

**Gonna Git Housed** — a Django app for renters and property managers to list homes, apply, and manage the rental process.

This is the HouseMe product (this Django repo). Titles and copy use HouseMe / Gonna Git Housed.

## Local setup

Prerequisites: Python 3.12, PostgreSQL, optional Docker.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Set SECRET_KEY, DB_* (and DEBUG=True) in .env
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runserver
```

Docker: `docker compose up --build` (uses the same `DB_*` keys as `.env.example`).

`DEBUG` defaults to **False** when unset. Local `.env` must set `DEBUG=True`. When `DEBUG` is False, a placeholder `SECRET_KEY` (`change-me` / `your-secret-key-here`) raises `ImproperlyConfigured`.

## Deploy on Render (one live URL)

The repo includes a Blueprint at [`render.yaml`](render.yaml): one Python web service + managed Postgres.

1. Merge this branch to `main` (or point Render at this branch).
2. In the [Render Dashboard](https://dashboard.render.com): **New → Blueprint**.
3. Connect **caradmico/RentMe** and select the branch that contains `render.yaml`.
4. Render creates:
   - Web service `houseme` (`runtime: python`)
   - Postgres `houseme-db` (private network; `DATABASE_URL` + `DB_NAME` / `DB_USER` / `DB_PASSWORD`)
5. When prompted (`sync: false`):
   - **MAPBOX_ACCESS_TOKEN** — optional `pk.*` token; map tiles stay blank without it.
   - For a custom domain later, add `CSRF_TRUSTED_ORIGINS=https://your.domain` and that host to `ALLOWED_HOSTS` in the Dashboard. The first `*.onrender.com` URL does not need this (settings append `https://$RENDER_EXTERNAL_HOSTNAME`).
6. `SECRET_KEY` is auto-generated. Do not use `change-me`.
7. After the first deploy, the live URL is `https://<service>.onrender.com` (shown on the service page and as `RENDER_EXTERNAL_HOSTNAME`).

`preDeployCommand` (`python manage.py migrate --noinput`) requires a **paid** web plan (`starter` in the Blueprint). On a free web instance, move migrate into `buildCommand`.

### Env vars for live deploy

| Variable | Required | Source |
|---|---|---|
| `SECRET_KEY` | yes | Blueprint `generateValue` |
| `DEBUG` | yes | `False` |
| `DATABASE_URL` | yes on Render | Postgres `connectionString` (settings prefer this) |
| `DB_NAME` | local / Docker | Postgres `database` (also set on Render) |
| `DB_USER` | local / Docker | Postgres `user` |
| `DB_PASSWORD` | local / Docker | Postgres `password` |
| `DB_HOST` | local / Docker | `localhost` or `db` in Compose. **Not** mapped from Render (no `host` property); comes from `DATABASE_URL`. |
| `DB_PORT` | local / Docker | `5432` (same as host) |
| `ALLOWED_HOSTS` | yes | `.onrender.com` + auto `RENDER_EXTERNAL_HOSTNAME` |
| `CSRF_TRUSTED_ORIGINS` | custom domain | comma-separated origins **with scheme**; Render hostname is auto-appended |
| `RENDER_EXTERNAL_HOSTNAME` | injected | Do not set; Render provides it |
| `MAPBOX_ACCESS_TOKEN` | optional | Dashboard prompt |
| `EMAIL_BACKEND` | optional | console by default |
| `DEFAULT_FROM_EMAIL` | optional | |
| `CONTACT_EMAIL` | optional | |
| `PYTHON_VERSION` | Blueprint | `3.12.8` |
| `DJANGO_SETTINGS_MODULE` | Blueprint | `houseme_project.settings` |

Build: `pip install -r requirements.txt && python manage.py collectstatic --noinput`  
Start: `gunicorn houseme_project.wsgi:application --bind 0.0.0.0:$PORT`  
Release: `python manage.py migrate --noinput`

## Features

- Renter and owner registration / login
- Property listings and a Mapbox map
- Applications and an admin approval flow
- Contact form (console email backend unless you configure SMTP)

## License

MIT — see [LICENSE](LICENSE) if present.
