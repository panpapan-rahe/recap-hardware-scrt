from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.perangkat import Perangkat
from app.models.cabang import Cabang
from app.models.kategori import Kategori
from app.models.aktivitas import Aktivitas


def generate_kode_unik(db: Session, cabang_id: int, kategori_id: int) -> str:
    cabang = db.query(Cabang).filter(Cabang.id == cabang_id).first()
    kategori = db.query(Kategori).filter(Kategori.id == kategori_id).first()
    prefix = kategori.nama[:3].upper() if kategori else "DEV"
    count = db.query(func.count(Perangkat.id)).scalar() + 1
    return f"{cabang.kode}-{prefix}-{count:04d}"


def compose_nama(merk: str | None, model: str | None) -> str:
    parts = [p.strip() for p in [merk or "", model or ""] if p and p.strip()]
    return " ".join(parts) if parts else "Perangkat"


def create_perangkat(db: Session, data: dict) -> Perangkat:
    kode = generate_kode_unik(db, data["cabang_id"], data["kategori_id"])
    payload = dict(data)
    payload["nama"] = compose_nama(payload.get("merk"), payload.get("model"))
    perangkat = Perangkat(**payload, kode_unik=kode)
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
    perangkat.nama = compose_nama(perangkat.merk, perangkat.model)
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


# FASE 2: Aktivitas
def pindah_cabang(db: Session, perangkat_id: int, cabang_tujuan_id: int, user_id: int, deskripsi: str = None) -> Perangkat | None:
    perangkat = get_perangkat_by_id(db, perangkat_id)
    if not perangkat:
        return None
    cabang_asal_id = perangkat.cabang_id
    status_sebelumnya = perangkat.status

    perangkat.cabang_id = cabang_tujuan_id
    db.commit()
    db.refresh(perangkat)

    aktivitas = Aktivitas(
        perangkat_id=perangkat_id,
        tipe="pindah",
        deskripsi=deskripsi or f"Pindah dari cabang {cabang_asal_id} ke {cabang_tujuan_id}",
        user_id=user_id,
        cabang_asal_id=cabang_asal_id,
        cabang_tujuan_id=cabang_tujuan_id,
        status_sebelumnya=status_sebelumnya,
        status_baru=perangkat.status,
    )
    db.add(aktivitas)
    db.commit()
    return perangkat


def pinjam_perangkat(db: Session, perangkat_id: int, peminjam: str, user_id: int, deskripsi: str = None) -> Perangkat | None:
    perangkat = get_perangkat_by_id(db, perangkat_id)
    if not perangkat:
        return None
    status_sebelumnya = perangkat.status

    perangkat.status = "dipinjam"
    db.commit()
    db.refresh(perangkat)

    aktivitas = Aktivitas(
        perangkat_id=perangkat_id,
        tipe="peminjaman",
        deskripsi=deskripsi or f"Dipinjam oleh {peminjam}",
        user_id=user_id,
        peminjam=peminjam,
        status_sebelumnya=status_sebelumnya,
        status_baru="dipinjam",
    )
    db.add(aktivitas)
    db.commit()
    return perangkat


def kembalikan_perangkat(db: Session, perangkat_id: int, user_id: int, deskripsi: str = None) -> Perangkat | None:
    perangkat = get_perangkat_by_id(db, perangkat_id)
    if not perangkat:
        return None
    status_sebelumnya = perangkat.status

    perangkat.status = "aktif"
    db.commit()
    db.refresh(perangkat)

    aktivitas = Aktivitas(
        perangkat_id=perangkat_id,
        tipe="pengembalian",
        deskripsi=deskripsi or "Perangkat dikembalikan",
        user_id=user_id,
        status_sebelumnya=status_sebelumnya,
        status_baru="aktif",
    )
    db.add(aktivitas)
    db.commit()
    return perangkat


def maintenance_perangkat(db: Session, perangkat_id: int, user_id: int, deskripsi: str = None) -> Perangkat | None:
    perangkat = get_perangkat_by_id(db, perangkat_id)
    if not perangkat:
        return None
    status_sebelumnya = perangkat.status

    perangkat.status = "maintenance"
    db.commit()
    db.refresh(perangkat)

    aktivitas = Aktivitas(
        perangkat_id=perangkat_id,
        tipe="maintenance",
        deskripsi=deskripsi or "Masuk maintenance",
        user_id=user_id,
        status_sebelumnya=status_sebelumnya,
        status_baru="maintenance",
    )
    db.add(aktivitas)
    db.commit()
    return perangkat


def selesai_maintenance(db: Session, perangkat_id: int, user_id: int, deskripsi: str = None) -> Perangkat | None:
    perangkat = get_perangkat_by_id(db, perangkat_id)
    if not perangkat:
        return None
    status_sebelumnya = perangkat.status

    perangkat.status = "aktif"
    db.commit()
    db.refresh(perangkat)

    aktivitas = Aktivitas(
        perangkat_id=perangkat_id,
        tipe="selesai_maintenance",
        deskripsi=deskripsi or "Maintenance selesai, kembali aktif",
        user_id=user_id,
        status_sebelumnya=status_sebelumnya,
        status_baru="aktif",
    )
    db.add(aktivitas)
    db.commit()
    return perangkat
