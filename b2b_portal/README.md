# B2B-Kundenportal

Professionelles Webportal für Unternehmen mit Rollenverwaltung, Rechnungsarchiv, Ticket-System, REST-API und Hintergrundjobs.

## Features
- Rollen: Admin, Kunde, Support (Custom `User`)
- Rechnungsarchiv: PDF-Upload/Download
- Ticket-System: Status + Kommentare
- REST-API: DRF + Token Auth
- Dashboard: Statistiken für Admin/Kunden
- Hintergrundjobs: Celery + Redis

## Schnellstart
1. Python 3.11+ installieren und virtualenv aktivieren
2. Abhängigkeiten installieren
   ```bash
   pip install -r requirements.txt
   ```
3. `.env` aus Vorlage erstellen und MySQL/Redis konfigurieren
   ```bash
   copy .env.example .env  # Windows
   # oder
   cp .env.example .env    # macOS/Linux
   ```
4. Datenbank vorbereiten und migrieren
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```
5. Entwicklungserver starten
   ```bash
   python manage.py runserver
   ```
6. Celery Worker starten (separates Terminal)
   ```bash
   celery -A core.celery_app worker -l info
   ```

## Docker-Setup
1. `.env` prüfen/erweitern (siehe `b2b_portal/.env.example`).
2. Starten:
   ```bash
   docker compose up --build
   ```
3. Erstmals Superuser anlegen (in Container ausführen):
   ```bash
   docker compose exec web python manage.py createsuperuser
   ```
4. App: http://localhost:8000, Admin: http://localhost:8000/admin

Services: `db` (MySQL 8), `redis` (Redis 7), `web` (Django via gunicorn), `worker` (Celery).

## Environment Variablen (`.env`)
- `DJANGO_SECRET_KEY` – Geheimschlüssel
- `DJANGO_DEBUG` – `1` (dev) oder `0` (prod)
- `DJANGO_ALLOWED_HOSTS` – z. B. `localhost,127.0.0.1`
- `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_DATABASE`, `MYSQL_USER`, `MYSQL_PASSWORD`
- `CELERY_BROKER_URL` – z. B. `redis://localhost:6379/0`
- `CELERY_RESULT_BACKEND` – z. B. `redis://localhost:6379/1`

## API
- Token holen: `POST /api/token/` mit `username`, `password`
- Endpunkte: `/api/users/`, `/api/invoices/`, `/api/tickets/`
- Paginierung: `page` (1-basiert), Größe via `API_PAGE_SIZE` (Default 20)
- Filter Beispiele:
  - Rechnungen: `number__icontains=R-1`, `invoice_date__gte=2024-01-01`, `amount__lte=100`
  - Tickets: `status=open`, `created_at__gte=2024-01-01`
  - Sortierung: `ordering=invoice_date` bzw. `ordering=-created_at`

## Ordnerstruktur
Siehe Projekt.

## Hinweise
- `AUTH_USER_MODEL` ist `accounts.User` – vor Migrationen nicht ändern.
- Datei-Uploads (Rechnungen) landen unter `media/`.
- Für produktiven Betrieb: STATIC/MEDIA via Webserver, sichere Secrets, Debug=0.
- Rollen & Schutz: Custom Decorator `accounts.roles.role_required(["admin","support"])`, Template-Filter `user|has_role:"admin"`.
- E-Mail Versand: Celery-Task `invoices.tasks.send_invoice_email(invoice_id)` – löst Admin-Aktion im Django-Admin aus oder via Upload-View.
