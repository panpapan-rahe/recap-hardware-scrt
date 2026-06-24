# Recap Hardware — Asset Management System

## 📋 Ringkasan

Sistem pencatatan perangkat IT untuk 4-6 cabang, dengan fitur CRUD perangkat, tracking aktivitas (pindah, peminjaman, maintenance, mutasi), dan report/export.

| Aspek | Detail |
|---|---|
| **Users** | Open, login untuk tracking siapa input |
| **Perangkat** | PC, Laptop, Printer, Router, Switch, POS, dll |
| **Cabang** | 4-6 cabang, ratusan-ribuan perangkat |
| **Deploy** | Home server (Docker Compose) → nanti pindah ke server kantor |
| **Akses** | Browser, responsive (mobile-friendly) |

---

## 🏗️ Arsitektur

| Layer | Tech | Alasan |
|---|---|---|
| **Backend** | Python (FastAPI) | Ringan, async, mudah di-deploy |
| **Database** | SQLite (awal) → PostgreSQL (kantor) | Simpel untuk dev, scalable untuk production |
| **Frontend** | HTML + CSS + JS (Alpine.js) | Ringan, reactive, tanpa build step |
| **Auth** | JWT token | Stateless, cocok untuk API |
| **Deploy** | Docker Compose | Tinggal `docker-compose up` di server mana pun |

---

## 📁 Struktur Folder

```
recap-hardware-scrt/
├── plan.md                          # Dokumen ini
├── docker-compose.yml               # Orkestrasi container
├── Dockerfile                       # Image backend
├── .env.example                     # Template environment variables
├── requirements.txt                 # Python dependencies
│
├── app/
│   ├── __init__.py
│   ├── main.py                      # Entry point FastAPI
│   ├── config.py                    # Config via environment variables
│   ├── database.py                  # DB connection & session
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py                  # Tabel User
│   │   ├── cabang.py                # Tabel Cabang
│   │   ├── kategori.py              # Tabel Kategori Perangkat
│   │   ├── perangkat.py             # Tabel Perangkat
│   │   └── aktivitas.py             # Tabel Log Aktivitas
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py                  # Schema User (request/response)
│   │   ├── cabang.py                # Schema Cabang
│   │   ├── kategori.py              # Schema Kategori
│   │   ├── perangkat.py             # Schema Perangkat
│   │   └── aktivitas.py             # Schema Aktivitas
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py                  # /auth/login, /auth/logout
│   │   ├── cabang.py                # /cabang
│   │   ├── kategori.py              # /kategori
│   │   ├── perangkat.py             # /perangkat
│   │   └── aktivitas.py             # /aktivitas
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py          # Logic auth (JWT, password hash)
│   │   ├── perangkat_service.py     # Logic CRUD perangkat
│   │   └── aktivitas_service.py     # Logic log aktivitas
│   └── templates/
│       └── index.html               # Single page (Alpine.js handles routing)
│
├── static/
│   ├── css/
│   │   └── style.css                # Custom styles
│   └── js/
│       └── app.js                   # Frontend logic (Alpine.js)
│
└── tests/
    ├── __init__.py
    ├── test_auth.py
    ├── test_perangkat.py
    └── test_aktivitas.py
```

---

## 🗄️ Database Schema

### Tabel: `users`
| Field | Type | Keterangan |
|---|---|---|
| id | INTEGER PK | Auto increment |
| username | VARCHAR(50) UNIQUE | |
| password_hash | VARCHAR(255) | bcrypt |
| nama_lengkap | VARCHAR(100) | |
| role | VARCHAR(20) | admin / viewer |
| created_at | DATETIME | |

### Tabel: `cabang`
| Field | Type | Keterangan |
|---|---|---|
| id | INTEGER PK | Auto increment |
| kode | VARCHAR(10) UNIQUE | BR01, BR02, dll |
| nama | VARCHAR(100) | |
| alamat | TEXT | |
| created_at | DATETIME | |

### Tabel: `kategori`
| Field | Type | Keterangan |
|---|---|---|
| id | INTEGER PK | Auto increment |
| nama | VARCHAR(50) | Laptop, PC, Printer, Router, Switch, POS |
| deskripsi | TEXT | |
| created_at | DATETIME | |

### Tabel: `perangkat`
| Field | Type | Keterangan |
|---|---|---|
| id | INTEGER PK | Auto increment |
| kode_unik | VARCHAR(20) | Auto-generate: BR01-LAP-0001 |
| nama | VARCHAR(100) | |
| kategori_id | FK → kategori | |
| merk | VARCHAR(50) | |
| model | VARCHAR(50) | |
| serial_number | VARCHAR(100) | |
| tahun_beli | INTEGER | |
| status | VARCHAR(20) | aktif / dipinjam / maintenance / mutasi / retired |
| cabang_id | FK → cabang | Lokasi saat ini |
| lokasi_detail | VARCHAR(200) | Ruangan/lantai |
| created_at | DATETIME | |
| updated_at | DATETIME | |

### Tabel: `aktivitas`
| Field | Type | Keterangan |
|---|---|---|
| id | INTEGER PK | Auto increment |
| perangkat_id | FK → perangkat | |
| tipe | VARCHAR(30) | pindah / peminjaman / maintenance / mutasi / penambahan |
| deskripsi | TEXT | |
| user_id | FK → user | Siapa yang catat |
| cabang_asal_id | FK → cabang | Untuk pindah/mutasi |
| cabang_tujuan_id | FK → cabang | Untuk pindah/mutasi |
| peminjam | VARCHAR(100) | Untuk peminjaman |
| status_sebelumnya | VARCHAR(20) | |
| status_baru | VARCHAR(20) | |
| created_at | DATETIME | |

---

## 🔄 Fase Development

### Fase 1: Foundation + CRUD Perangkat
- [ ] Setup project (struktur folder, requirements.txt, Dockerfile, docker-compose.yml)
- [ ] Database connection & models (SQLAlchemy)
- [ ] Auth (register, login, JWT middleware)
- [ ] Master data: Cabang CRUD
- [ ] Master data: Kategori CRUD
- [ ] Perangkat CRUD (tambah, lihat, edit, hapus)
- [ ] Auto-generate kode unik perangkat
- [ ] Dashboard sederhana (total perangkat per cabang)
- [ ] Responsive UI (CSS framework)
- [ ] Seed data awal (admin user, cabang, kategori)

### Fase 2: Aktivitas Tracking
- [ ] Pindah cabang (dari → ke, siapa catat)
- [ ] Peminjaman (dipinjam oleh siapa, dari → ke)
- [ ] Maintenance (jenis, deskripsi, biaya, selesai kapan)
- [ ] Mutasi (penghapusan/penyerahan ke pihak lain)
- [ ] Log aktivitas per perangkat

### Fase 3: Report & Export
- [ ] Export per cabang (PDF/Excel)
- [ ] Export per kategori
- [ ] Riwayat per perangkat
- [ ] Log aktivitas per periode
- [ ] Dashboard charts

### Fase 4: Polish & Deploy
- [ ] Testing
- [ ] Optimasi performa
- [ ] Migrasi ke PostgreSQL
- [ ] Docker production setup
- [ ] Documentation

---

## 🔐 API Endpoints (Fase 1)

### Auth
| Method | Endpoint | Deskripsi |
|---|---|---|
| POST | /auth/register | Register user baru |
| POST | /auth/login | Login, return JWT |
| GET | /auth/me | Info user yang login |

### Cabang
| Method | Endpoint | Deskripsi |
|---|---|---|
| GET | /cabang | Daftar semua cabang |
| POST | /cabang | Tambah cabang |
| PUT | /cabang/{id} | Edit cabang |
| DELETE | /cabang/{id} | Hapus cabang |

### Kategori
| Method | Endpoint | Deskripsi |
|---|---|---|
| GET | /kategori | Daftar semua kategori |
| POST | /kategori | Tambah kategori |
| PUT | /kategori/{id} | Edit kategori |
| DELETE | /kategori/{id} | Hapus kategori |

### Perangkat
| Method | Endpoint | Deskripsi |
|---|---|---|
| GET | /perangkat | Daftar perangkat (filter by cabang, kategori, status) |
| GET | /perangkat/{id} | Detail perangkat |
| POST | /perangkat | Tambah perangkat |
| PUT | /perangkat/{id} | Edit perangkat |
| DELETE | /perangkat/{id} | Hapus perangkat |

### Dashboard
| Method | Endpoint | Deskripsi |
|---|---|---|
| GET | /dashboard/stats | Statistik perangkat per cabang & kategori |

---

## 🚀 Deployment

### Docker Compose (dev)
```yaml
services:
  app:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./app:/app
      - ./data:/app/data  # SQLite DB
    environment:
      - DATABASE_URL=sqlite:///app/data/db.sqlite3
      - SECRET_KEY=change-me-in-production
```

### Migrasi ke Production (kantor)
1. Ganti SQLite → PostgreSQL di `docker-compose.yml`
2. Update `DATABASE_URL`
3. Jalankan migration (SQLAlchemy create_all)
4. Import data dari SQLite ke PostgreSQL

---

## 📝 Catatan

- **Frontend**: Single HTML file + Alpine.js untuk reactivity tanpa build step. Cocok untuk project skala ini.
- **Auth**: JWT disimpan di localStorage, dikirim via Authorization header.
- **Kode Unik**: Format `{KODE_CABANG}-{KATEGORI_PREFIX}-{SEQUENTIAL}`, contoh: `BR01-LAP-0001`
- **Responsive**: CSS custom, mobile-first approach.
