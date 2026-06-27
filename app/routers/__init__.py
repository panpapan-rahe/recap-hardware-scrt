from app.routers.auth import router as auth_router
from app.routers.cabang import router as cabang_router
from app.routers.kategori import router as kategori_router
from app.routers.perangkat import router as perangkat_router
from app.routers.aktivitas import router as aktivitas_router
from app.routers.report import router as report_router
from app.routers.admin import router as admin_router

__all__ = ["auth_router", "cabang_router", "kategori_router", "perangkat_router", "aktivitas_router", "report_router", "admin_router"]
