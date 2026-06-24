from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.kategori import Kategori
from app.schemas.kategori import KategoriCreate, KategoriUpdate, KategoriResponse
from app.deps import get_current_user_id

router = APIRouter(prefix="/kategori", tags=["Kategori"])


@router.get("/", response_model=list[KategoriResponse])
def list_kategori(db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    return db.query(Kategori).order_by(Kategori.nama).all()


@router.post("/", response_model=KategoriResponse)
def create_kategori(data: KategoriCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    kategori = Kategori(**data.model_dump())
    db.add(kategori)
    db.commit()
    db.refresh(kategori)
    return kategori


@router.put("/{kategori_id}", response_model=KategoriResponse)
def update_kategori(kategori_id: int, data: KategoriUpdate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    kategori = db.query(Kategori).filter(Kategori.id == kategori_id).first()
    if not kategori:
        raise HTTPException(status_code=404, detail="Kategori tidak ditemukan")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(kategori, key, value)
    db.commit()
    db.refresh(kategori)
    return kategori


@router.delete("/{kategori_id}")
def delete_kategori(kategori_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    kategori = db.query(Kategori).filter(Kategori.id == kategori_id).first()
    if not kategori:
        raise HTTPException(status_code=404, detail="Kategori tidak ditemukan")
    db.delete(kategori)
    db.commit()
    return {"message": "Kategori berhasil dihapus"}
