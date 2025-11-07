# B2B‑Kundenportal (Django + DRF + Celery + Docker)

Ein professionelles Webportal für Geschäftskunden. Kunden sehen Rechnungen, erstellen Support‑Tickets und kommunizieren mit dem Unternehmen; Admin/Support verwalten Benutzer, Rechnungen, Tickets und E‑Mails. Der Code ist modular, produktionsnah und Docker‑fähig – ideal als Referenzprojekt in Bewerbungen.

## Highlights
- Rollenbasiert: Admin, Kunde, Support (Custom User)
- Rechnungsarchiv mit PDF‑Upload/Download und Admin‑Zuweisung
- Ticket‑System mit Status und Kommentaren
- REST‑API (Token‑Auth, Filter, Suche, Sortierung, Pagination)
- Admin‑UI in modernem Design (Jazzmin), WhiteNoise für Static Files
- Hintergrundjobs mit Celery + Redis (z. B. Rechnungs‑E‑Mail)
- Docker‑Setup: MySQL, Redis, Web (Gunicorn), Worker

## Tech Stack
- Backend: Django 5, Django REST Framework
- Datenbank: MySQL 8 (lokal optional SQLite)
- Background: Celery 5 + Redis 7
- Frontend‑Basis: Bootstrap (Templates) + Jazzmin im Admin
- Container: Dockerfile, docker‑compose

## Schnellstart (Docker)
1) `.env` erstellen (siehe `b2b_portal/.env.example`).
2) Starten:
   ```bash
   docker compose up -d --build
   docker compose exec web python manage.py createsuperuser
   ```
3) Öffnen:
   - App: http://localhost:8000
   - Admin: http://localhost:8000/admin

Hinweise:
- E‑Mails werden im Console‑Backend geloggt (siehe `docker compose logs -f web`).
- Port‑Konflikte mit lokalem MySQL/Redis? Entweder lokale Dienste stoppen oder `ports:` bei `db`/`redis` entfernen.

## REST‑API
- Token: `POST /api/token/` mit `username`, `password`
- Endpunkte: `/api/users/` (nur Admin), `/api/invoices/`, `/api/tickets/`
- Paginierung: `page=1` (Größe via `API_PAGE_SIZE`)
- Filter/Sortierung (Beispiele):
  - Rechnungen: `number__icontains=R-1`, `invoice_date__gte=2024-01-01`, `amount__lte=100`
  - Tickets: `status=open`, `created_at__gte=2024-01-01`
  - Sortierung: `ordering=invoice_date` bzw. `ordering=-created_at`

## Rollen & Berechtigungen
- Decorator: `accounts.roles.role_required(["admin", "support"])`
- Template‑Filter: `user|has_role:"admin"`
- Sichtbarkeit UI: Kunden sehen nur eigene Daten; Admin/Support sehen alles.

## Projektstruktur (Ausschnitt)
```
b2b_portal/
├─ accounts/      # Benutzer & Rollen (Custom User)
├─ invoices/      # Rechnungen, Upload, Admin‑Aktionen, E‑Mail‑Task
├─ tickets/       # Tickets, Kommentare
├─ dashboard/     # Admin/Kunden‑Dashboards
├─ api/           # DRF Serializer, ViewSets, Router
├─ core/          # Settings, URLs, ASGI/WSGI, Celery App
├─ templates/     # HTML (Bootstrap + E‑Mail‑Vorlagen)
├─ static/        # CSS/JS/Images (inkl. Admin‑Branding)
└─ manage.py
```

## Entwicklung ohne Docker (optional, SQLite)
```bash
# Windows PowerShell
cd b2b_portal
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
# optional: lokale Settings für SQLite
#   DJANGO_SETTINGS_MODULE=core.settings (Default nutzt MySQL)
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Screenshots
- Admin (Jazzmin) – modernisiertes Backend
- Kunden‑Dashboard, Rechnungs‑Liste, Ticket‑Ansicht

(Hinweis: Screenshots können nach Deployment ergänzt werden.)

## Warum dieses Projekt?
- Zeigt ganzheitliche Web‑Entwicklung: Auth, UI, API, Background‑Jobs, Docker.
- Klare, erweiterbare Architektur und saubere Trennung der Domänen.
- Praxisrelevante Features (Rechnungen, Tickets, E‑Mail) mit realistischen Technologien.

## Lizenz
Dieses Beispielprojekt ist ausschließlich zu Demonstrations‑ und Bewerbungszwecken gedacht. (Bei Bedarf kann eine OSS‑Lizenz ergänzt werden.)
