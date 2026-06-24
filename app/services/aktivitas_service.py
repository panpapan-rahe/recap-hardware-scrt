from sqlalchemy.orm import Session
from app.models.aktivitas import Aktivitas


def create_aktivitas(db: Session, data: dict, user_id: int) -> Aktivitas:
    aktivitas = Aktivitas(**data, user_id=user_id)
    db.add(aktivitas)
    db.commit()
    db.refresh(aktivitas)
    return aktivitas


def get_aktivitas_by_perangkat(db: Session, perangkat_id: int):
    return (
        db.query(Aktivitas)
        .filter(Aktivitas.perangkat_id == perangkat_id)
        .order_by(Aktivitas.created_at.desc())
        .all()
    )


def get_all_aktivitas(db: Session, limit: int = 100):
    return (
        db.query(Aktivitas)
        .order_by(Aktivitas.created_at.desc())
        .limit(limit)
        .all()
    )
