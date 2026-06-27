from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.perangkat import (
    PerangkatCreate, PerangkatUpdate, PerangkatResponse,
    PindahRequest, PinjamRequest, MaintenanceRequest,
)
from app.services.perangkat_service import (
    create_perangkat, get_perangkat_list, get_perangkat_by_id,
    update_perangkat, delete_perangkat, get_dashboard_stats,
    pindah_cabang, pinjam_perangkat, kembalikan_perangkat,
    maintenance_perangkat, selesai_maintenance,
)
from app.deps import get_current_user

router = APIRouter(prefix="/perangkat", tags=["Perangkat"])


@router.get("/", response_model=list[PerangkatResponse])
def list_perangkat(
    cabang_id: int = Query(None),
    kategori_id: int = Query(None),
    status: str = Query(None),
    db: Session = Depends(get_db),
):
    return get_perangkat_list(db, cabang_id, kategori_id, status)


@router.get("/{perangkat_id}", response_model=PerangkatResponse)
def detail_perangkat(perangkat_id: int, db: Session = Depends(get_db)):
    perangkat = get_perangkat_by_id(db, perangkat_id)
    if not perangkat:
        raise HTTPException(status_code=404, detail="Perangkat tidak ditemukan")
    return perangkat


@router.post("/", response_model=PerangkatResponse)
def add_perangkat(data: PerangkatCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return create_perangkat(db, data.model_dump())


@router.put("/{perangkat_id}", response_model=PerangkatResponse)
def edit_perangkat(perangkat_id: int, data: PerangkatUpdate, db: Session = Depends(get_db)):
    perangkat = update_perangkat(db, perangkat_id, data.model_dump(exclude_unset=True))
    if not perangkat:
        raise HTTPException(status_code=404, detail="Perangkat tidak ditemukan")
    return perangkat


@router.delete("/{perangkat_id}")
def remove_perangkat(perangkat_id: int, db: Session = Depends(get_db)):
    if not delete_perangkat(db, perangkat_id):
        raise HTTPException(status_code=404, detail="Perangkat tidak ditemukan")
    return {"message": "Perangkat berhasil dihapus"}


@router.get("/dashboard/stats")
def dashboard(db: Session = Depends(get_db)):
    return get_dashboard_stats(db)


# FASE 2: Aktivitas endpoints
@router.post("/{perangkat_id}/pindah")
def pindah(
    perangkat_id: int,
    data: PindahRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    result = pindah_cabang(db, perangkat_id, data.cabang_tujuan_id, user.id, data.deskripsi or "")
    if not result:
        raise HTTPException(status_code=404, detail="Perangkat tidak ditemukan")
    return {"message": "Perangkat berhasil dipindahkan", "perangkat": result}


@router.post("/{perangkat_id}/pinjam")
def pinjam(
    perangkat_id: int,
    data: PinjamRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    result = pinjam_perangkat(db, perangkat_id, data.peminjam, user.id, data.deskripsi or "")
    if not result:
        raise HTTPException(status_code=404, detail="Perangkat tidak ditemukan")
    return {"message": f"Perangkat dipinjam oleh {data.peminjam}", "perangkat": result}


@router.post("/{perangkat_id}/kembalikan")
def kembalikan(
    perangkat_id: int,
    data: MaintenanceRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    result = kembalikan_perangkat(db, perangkat_id, user.id, data.deskripsi or "")
    if not result:
        raise HTTPException(status_code=404, detail="Perangkat tidak ditemukan")
    return {"message": "Perangkat berhasil dikembalikan", "perangkat": result}


@router.post("/{perangkat_id}/maintenance")
def maintenance(
    perangkat_id: int,
    data: MaintenanceRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    result = maintenance_perangkat(db, perangkat_id, user.id, data.deskripsi or "")
    if not result:
        raise HTTPException(status_code=404, detail="Perangkat tidak ditemukan")
    return {"message": "Perangkat masuk maintenance", "perangkat": result}


@router.post("/{perangkat_id}/selesai-maintenance")
def selesai_maintenance_endpoint(
    perangkat_id: int,
    data: MaintenanceRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    result = selesai_maintenance(db, perangkat_id, user.id, data.deskripsi or "")
    if not result:
        raise HTTPException(status_code=404, detail="Perangkat tidak ditemukan")
    return {"message": "Maintenance selesai, perangkat aktif kembali", "perangkat": result}
