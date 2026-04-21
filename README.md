# MedTribute

MedTribute is a production-oriented Django 5 memorial platform for honoring deceased doctors.
It includes obituary pages, funeral events, condolence walls, donation handling for Uganda-focused payment flows, and real-time live tribute messaging via WebSockets.

## Stack
- Django 5 + Django REST Framework
- PostgreSQL
- Redis (cache + channels)
- Django Channels (WebSockets)
- Django Templates (responsive UI)
- Docker + Nginx + Gunicorn
- Optional AWS S3 media storage

## Project layout

```
apps/
  accounts/
  obituaries/
  donations/
  messaging/
  streaming/
medtribute/
templates/
static/
nginx/
```

## Key features implemented

### Obituaries
- Doctor obituary profiles with slug URLs (`/tribute/<slug>/`)
- Biography, specialty, hospital affiliations, dates, funeral details, map URL
- Search by name/specialty/hospital
- Filter obituaries by year/month via API

### Funeral events
- Wake/funeral/burial events attached to obituary records
- Web template includes upcoming event section

### Video features
- `Video` model supports: upload, YouTube Live, Vimeo, WebRTC metadata
- API endpoint for managing per-obituary video gallery

### Condolences
- Threaded condolence messages (`parent` relationship)
- Reactions (prayer/heart/support)
- Admin moderation via `approve` action
- Live tribute wall WebSocket endpoint:
  - `ws://<host>/ws/tributes/<slug>/`

### Donations
- Donation model supporting Flutterwave, MTN MoMo, Airtel Money
- Webhook verification scaffold for Flutterwave signature validation
- Donation summary endpoint (total + recent donors)
- Payout request model for organizer/admin workflows

### Auth & roles
- Custom user model (`accounts.User`) with roles:
  - `admin`
  - `family`
  - `user`
- JWT auth endpoints (`/api/token/`, `/api/token/refresh/`)

### Security / Ops
- DRF throttling for anti-spam
- Redis caching configured
- Secure cookie and proxy headers enabled
- Dockerized deployment with Nginx reverse proxy

---

## API endpoints (core)

- `POST /api/accounts/register/`
- `GET /api/accounts/me/`
- `POST /api/token/`
- `POST /api/token/refresh/`
- `GET/POST /api/obituaries/`
- `GET/POST /api/messages/`
- `GET/POST /api/donations/`
- `POST /api/donations/webhooks/flutterwave/`
- `GET/POST /api/streaming/videos/`

---

## Local setup

### 1) Environment
Copy and edit env:

```bash
cp .env.example .env
```

### 2) Run with Docker

```bash
docker compose up --build
```

### 3) Migrate + create superuser

```bash
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

### 4) Access
- App: `http://localhost/`
- Admin: `http://localhost/admin/`

---

## Notes for production hardening
- Replace placeholder secrets in `.env`
- Configure HTTPS (Let's Encrypt / cloud LB)
- Implement final MTN MoMo/Airtel API adapters and callback verification
- Add Celery for async receipts, reminders, SMS and email queues
- Add audit logging + GDPR consent/export/delete workflows
- Add full observability (Sentry, Prometheus, structured logs)

## Bonus extension ideas
- AI obituary summary generator
- Voice condolence uploads
- QR code per tribute page
- Digital candle lighting interaction
