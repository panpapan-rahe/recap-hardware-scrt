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
from app.models.aktivitas import Aktivitas
from app.models.kategori import Kategori

router = APIRouter(tags=["Perangkat"])


def enrich_perangkat_response(db: Session, perangkat) -> dict:
    data = PerangkatResponse.model_validate(perangkat).model_dump()
    kategori = db.query(Kategori).filter(Kategori.id == perangkat.kategori_id).first() if perangkat.kategori_id else None
    data["kategori_nama"] = kategori.nama if kategori else None
    return data


@router.get("/", response_model=list[PerangkatResponse])
def list_perangkat(
    cabang_id: int = Query(None),
    kategori_id: int = Query(None),
    status: str = Query(None),
    db: Session = Depends(get_db),
):
    perangkat_list = get_perangkat_list(db, cabang_id, kategori_id, status)
    return [enrich_perangkat_response(db, p) for p in perangkat_list]


@router.get("/{perangkat_id}", response_model=PerangkatResponse)
def detail_perangkat(perangkat_id: int, db: Session = Depends(get_db)):
    perangkat = get_perangkat_by_id(db, perangkat_id)
    if not perangkat:
        raise HTTPException(status_code=404, detail="Perangkat tidak ditemukan")
    return enrich_perangkat_response(db, perangkat)


@router.post("/", response_model=PerangkatResponse)
def add_perangkat(data: PerangkatCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    perangkat = create_perangkat(db, data.model_dump(), user.id)
    return enrich_perangkat_response(db, perangkat)


@router.put("/{perangkat_id}", response_model=PerangkatResponse)
def edit_perangkat(perangkat_id: int, data: PerangkatUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    perangkat = get_perangkat_by_id(db, perangkat_id)
    if not perangkat:
        raise HTTPException(status_code=404, detail="Perangkat tidak ditemukan")
    
    update_data = data.model_dump(exclude_unset=True)
    perangkat = update_perangkat(db, perangkat_id, update_data)
    
    # Log aktivitas
    changes = []
    if "status" in update_data:
        changes.append(f"status: {perangkat.status} → {update_data['status']}")
    if changes:
        aktivitas = Aktivitas(
            perangkat_id=perangkat_id,
            tipe="edit",
            deskripsi=f"Perangkat diedit: {perangkat.nama} ({', '.join(changes)})",
            user_id=user.id,
            status_sebelumnya=perangkat.status,
            status_baru=update_data.get("status"),
        )
        db.add(aktivitas)
        db.commit()
    
    return enrich_perangkat_response(db, perangkat)


@router.delete("/{perangkat_id}")
def remove_perangkat(perangkat_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    perangkat = get_perangkat_by_id(db, perangkat_id)
    if not perangkat:
        raise HTTPException(status_code=404, detail="Perangkat tidak ditemukan")
    
    # Log aktivitas sebelum hapus
    aktivitas = Aktivitas(
        perangkat_id=perangkat_id,
        tipe="hapus",
        deskripsi=f"Perangkat dihapus: {perangkat.nama} ({perangkat.kode_unik})",
        user_id=user.id,
        status_sebelumnya=perangkat.status,
    )
    db.add(aktivitas)
    
    db.delete(perangkat)
    db.commit()
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
