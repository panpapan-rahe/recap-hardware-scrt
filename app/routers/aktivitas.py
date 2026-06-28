from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.aktivitas import AktivitasCreate, AktivitasResponse
from app.services.aktivitas_service import create_aktivitas, get_aktivitas_by_perangkat, get_all_aktivitas
from app.deps import get_current_user

router = APIRouter(tags=["Aktivitas"])


@router.get("/perangkat/{perangkat_id}", response_model=list[AktivitasResponse])
def list_aktivitas_perangkat(perangkat_id: int, db: Session = Depends(get_db)):
    return get_aktivitas_by_perangkat(db, perangkat_id)


@router.get("/", response_model=list[AktivitasResponse])
def list_all_aktivitas(tipe: str = Query(None), db: Session = Depends(get_db)):
    return get_all_aktivitas(db, tipe=tipe)


@router.post("/", response_model=AktivitasResponse)
def add_aktivitas(data: AktivitasCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return create_aktivitas(db, data.model_dump(), user.id)
