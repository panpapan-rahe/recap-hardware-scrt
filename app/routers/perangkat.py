from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.perangkat import PerangkatCreate, PerangkatUpdate, PerangkatResponse
from app.services.perangkat_service import (
    create_perangkat, get_perangkat_list, get_perangkat_by_id,
    update_perangkat, delete_perangkat, get_dashboard_stats,
)
from app.deps import get_current_user_id

router = APIRouter(prefix="/perangkat", tags=["Perangkat"])


@router.get("/", response_model=list[PerangkatResponse])
def list_perangkat(
    cabang_id: int = Query(None),
    kategori_id: int = Query(None),
    status: str = Query(None),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    return get_perangkat_list(db, cabang_id, kategori_id, status)


@router.get("/{perangkat_id}", response_model=PerangkatResponse)
def detail_perangkat(perangkat_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    perangkat = get_perangkat_by_id(db, perangkat_id)
    if not perangkat:
        raise HTTPException(status_code=404, detail="Perangkat tidak ditemukan")
    return perangkat


@router.post("/", response_model=PerangkatResponse)
def add_perangkat(data: PerangkatCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    return create_perangkat(db, data.model_dump())


@router.put("/{perangkat_id}", response_model=PerangkatResponse)
def edit_perangkat(perangkat_id: int, data: PerangkatUpdate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    perangkat = update_perangkat(db, perangkat_id, data.model_dump(exclude_unset=True))
    if not perangkat:
        raise HTTPException(status_code=404, detail="Perangkat tidak ditemukan")
    return perangkat


@router.delete("/{perangkat_id}")
def remove_perangkat(perangkat_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    if not delete_perangkat(db, perangkat_id):
        raise HTTPException(status_code=404, detail="Perangkat tidak ditemukan")
    return {"message": "Perangkat berhasil dihapus"}


@router.get("/dashboard/stats")
def dashboard(db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    return get_dashboard_stats(db)
