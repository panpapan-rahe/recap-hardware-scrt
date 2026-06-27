from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.cabang import Cabang
from app.schemas.cabang import CabangCreate, CabangUpdate, CabangResponse
from app.deps import require_admin, get_current_user

router = APIRouter(tags=["Cabang"])


@router.get("/", response_model=list[CabangResponse])
def list_cabang(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(Cabang).order_by(Cabang.kode).all()


@router.post("/", response_model=CabangResponse)
def create_cabang(data: CabangCreate, db: Session = Depends(get_db), admin=Depends(require_admin)):
    cabang = Cabang(**data.model_dump())
    db.add(cabang)
    db.commit()
    db.refresh(cabang)
    return cabang


@router.put("/{cabang_id}", response_model=CabangResponse)
def update_cabang(cabang_id: int, data: CabangUpdate, db: Session = Depends(get_db), admin=Depends(require_admin)):
    cabang = db.query(Cabang).filter(Cabang.id == cabang_id).first()
    if not cabang:
        raise HTTPException(status_code=404, detail="Cabang tidak ditemukan")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(cabang, key, value)
    db.commit()
    db.refresh(cabang)
    return cabang


@router.delete("/{cabang_id}")
def delete_cabang(cabang_id: int, db: Session = Depends(get_db), admin=Depends(require_admin)):
    cabang = db.query(Cabang).filter(Cabang.id == cabang_id).first()
    if not cabang:
        raise HTTPException(status_code=404, detail="Cabang tidak ditemukan")
    db.delete(cabang)
    db.commit()
    return {"message": "Cabang berhasil dihapus"}
