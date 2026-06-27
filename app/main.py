from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import HTMLResponse
import os

from app.database import engine, Base
from app.routers import (
    auth_router,
    cabang_router,
    kategori_router,
    perangkat_router,
    aktivitas_router,
    report_router,
    admin_router,
)
from app.config import DATABASE_URL

# Buat folder data jika pakai SQLite
if "sqlite" in DATABASE_URL:
    data_dir = os.path.dirname(DATABASE_URL.replace("sqlite:///", ""))
    if data_dir:
        os.makedirs(data_dir, exist_ok=True)

# Buat tabel jika belum ada
Base.metadata.create_all(bind=engine)


def ensure_sqlite_schema():
    if "sqlite" not in DATABASE_URL:
        return
    with engine.begin() as conn:
        cols = conn.exec_driver_sql("PRAGMA table_info(perangkat)").fetchall()
        col_names = {row[1] for row in cols}
        if "adjuro" not in col_names:
            conn.exec_driver_sql("ALTER TABLE perangkat ADD COLUMN adjuro VARCHAR(100)")

        cabang_cols = conn.exec_driver_sql("PRAGMA table_info(cabang)").fetchall()
        cabang_names = {row[1] for row in cabang_cols}
        if "inisial" not in cabang_names:
            conn.exec_driver_sql("ALTER TABLE cabang ADD COLUMN inisial VARCHAR(10)")


ensure_sqlite_schema()

app = FastAPI(title="Recap Hardware", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Register routers
app.include_router(auth_router, prefix="/api")
app.include_router(cabang_router, prefix="/api")
app.include_router(kategori_router, prefix="/api")
app.include_router(perangkat_router, prefix="/api")
app.include_router(aktivitas_router, prefix="/api")
app.include_router(report_router, prefix="/api")
app.include_router(admin_router, prefix="/api")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request=request, name="dashboard.html")

@app.get("/login.html", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")

@app.get("/dashboard.html", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse(request=request, name="dashboard.html")

@app.get("/cabang.html", response_class=HTMLResponse)
def cabang_page(request: Request):
    return templates.TemplateResponse(request=request, name="cabang.html")

@app.get("/perangkat.html", response_class=HTMLResponse)
def perangkat_page(request: Request):
    return templates.TemplateResponse(request=request, name="perangkat.html")

@app.get("/aktivitas.html", response_class=HTMLResponse)
def aktivitas_page(request: Request):
    return templates.TemplateResponse(request=request, name="aktivitas.html")

@app.get("/report.html", response_class=HTMLResponse)
def report_page(request: Request):
    return templates.TemplateResponse(request=request, name="report.html")

@app.get("/admin.html", response_class=HTMLResponse)
def admin_page(request: Request):
    return templates.TemplateResponse(request=request, name="admin.html")


@app.get("/health")
def health():
    return {"status": "ok"}
