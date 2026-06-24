from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.perangkat import Perangkat
from app.models.cabang import Cabang
from app.models.kategori import Kategori


def generate_kode_unik(db: Session, cabang_id: int, kategori_id: int) -> str:
    cabang = db.query(Cabang).filter(Cabang.id == cabang_id).first()
    kategori = db.query(Kategori).filter(Kategori.id == kategori_id).first()
    prefix = kategori.nama[:3].upper() if kategori else "DEV"
    count = db.query(func.count(Perangkat.id)).scalar() + 1
    return f"{cabang.kode}-{prefix}-{count:04d}"


def create_perangkat(db: Session, data: dict) -> Perangkat:
    kode = generate_kode_unik(db, data["cabang_id"], data["kategori_id"])
    perangkat = Perangkat(**data, kode_unik=kode)
    db.add(perangkat)
    db.commit()
    db.refresh(perangkat)
    return perangkat


def get_perangkat_list(db: Session, cabang_id: int = None, kategori_id: int = None, status: str = None):
    query = db.query(Perangkat)
    if cabang_id:
        query = query.filter(Perangkat.cabang_id == cabang_id)
    if kategori_id:
        query = query.filter(Perangkat.kategori_id == kategori_id)
    if status:
        query = query.filter(Perangkat.status == status)
    return query.order_by(Perangkat.created_at.desc()).all()


def get_perangkat_by_id(db: Session, perangkat_id: int) -> Perangkat | None:
    return db.query(Perangkat).filter(Perangkat.id == perangkat_id).first()


def update_perangkat(db: Session, perangkat_id: int, data: dict) -> Perangkat | None:
    perangkat = get_perangkat_by_id(db, perangkat_id)
    if not perangkat:
        return None
    for key, value in data.items():
        if value is not None:
            setattr(perangkat, key, value)
    db.commit()
    db.refresh(perangkat)
    return perangkat


def delete_perangkat(db: Session, perangkat_id: int) -> bool:
    perangkat = get_perangkat_by_id(db, perangkat_id)
    if not perangkat:
        return False
    db.delete(perangkat)
    db.commit()
    return True


def get_dashboard_stats(db: Session) -> dict:
    total = db.query(func.count(Perangkat.id)).scalar()
    per_cabang = (
        db.query(Cabang.nama, func.count(Perangkat.id))
        .join(Perangkat, Perangkat.cabang_id == Cabang.id)
        .group_by(Cabang.nama)
        .all()
    )
    per_status = (
        db.query(Perangkat.status, func.count(Perangkat.id))
        .group_by(Perangkat.status)
        .all()
    )
    return {
        "total": total,
        "per_cabang": [{"nama": n, "jumlah": j} for n, j in per_cabang],
        "per_status": [{"status": s, "jumlah": j} for s, j in per_status],
    }
