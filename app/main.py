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
)
from app.config import DATABASE_URL

# Buat tabel jika belum ada
Base.metadata.create_all(bind=engine)

# Buat folder data jika pakai SQLite
if "sqlite" in DATABASE_URL:
    data_dir = os.path.dirname(DATABASE_URL.replace("sqlite:///", ""))
    if data_dir:
        os.makedirs(data_dir, exist_ok=True)

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


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
def health():
    return {"status": "ok"}
