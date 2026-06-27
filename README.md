# Recap Hardware SCRT

Sistem pencatatan perangkat IT untuk cabang, dengan fokus ke tracking aset, aktivitas perangkat, dan report/export.

## Fitur

### Fase 1
- Login / logout
- Dashboard ringkas
- CRUD Cabang
- CRUD Kategori perangkat
- CRUD Perangkat
- Responsive UI

### Fase 2
- Pindah cabang
- Peminjaman perangkat
- Pengembalian perangkat
- Maintenance perangkat
- Riwayat aktivitas per perangkat
- Log aktivitas global

### Fase 3
- Report data perangkat
- Export CSV
- Export PDF

## Tech Stack

- Backend: FastAPI
- Database: SQLite (dev)
- ORM: SQLAlchemy
- Frontend: HTML + CSS + Alpine.js
- Deployment: Docker Compose

## Struktur Singkat

- `app/main.py` — entry point FastAPI
- `app/models/` — model database
- `app/schemas/` — Pydantic schema
- `app/services/` — business logic
- `app/routers/` — API endpoints
- `templates/` — UI utama
- `static/` — CSS dan JS

## Menjalankan Project

### Dengan Docker Compose

```bash
docker-compose up -d
```

Akses aplikasi:

```bash
http://localhost:9103
```

## Login Default

```text
Username: admin
Password: admin123
```

## Endpoint Utama

Prefix API: `/api`

- `POST /api/auth/login`
- `GET /api/auth/me`
- `GET /api/cabang/`
- `GET /api/kategori/`
- `GET /api/perangkat/`
- `GET /api/perangkat/dashboard/stats`
- `GET /api/aktivitas/`
- `GET /api/report/data`
- `GET /api/report/export/csv`
- `GET /api/report/export/pdf`

## Catatan

- Database seed hanya membuat user admin, cabang, dan kategori.
- Data perangkat ditambahkan lewat UI atau API.
- Project ini dijalankan di port `9103`.

## Kebutuhan Lokal

Jika ingin rebuild manual:

```bash
docker-compose down
docker-compose build --no-cache app
docker-compose up -d
```

## Lisensi

Private/internal project.
