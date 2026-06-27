from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.aktivitas import Aktivitas
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.services.auth_service import (
    create_user, get_all_users, update_user, deactivate_user, get_user_by_id,
)
from app.deps import require_admin

router = APIRouter(tags=["Admin"])


@router.get("/users", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db), admin=Depends(require_admin)):
    return get_all_users(db)


@router.post("/users", response_model=UserResponse)
def add_user(data: UserCreate, db: Session = Depends(get_db), admin=Depends(require_admin)):
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(status_code=400, detail="Username sudah terdaftar")
    user = create_user(db, data.username, data.password, data.nama_lengkap, data.role or "pic")

    # Log aktivitas
    log = Aktivitas(
        tipe="tambah_user",
        deskripsi=f"Admin menambahkan user: {user.username} ({user.nama_lengkap}) sebagai {user.role}",
        user_id=admin.id,
        target_user_id=user.id,
    )
    db.add(log)
    db.commit()

    return user


@router.put("/users/{user_id}", response_model=UserResponse)
def edit_user(user_id: int, data: UserUpdate, db: Session = Depends(get_db), admin=Depends(require_admin)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")

    update_data = data.model_dump(exclude_unset=True)
    updated = update_user(db, user_id, **update_data)

    # Log aktivitas
    changes = []
    if data.nama_lengkap is not None:
        changes.append(f"nama: {user.nama_lengkap} → {data.nama_lengkap}")
    if data.role is not None:
        changes.append(f"role: {user.role} → {data.role}")
    if data.is_active is not None:
        status = "aktif" if data.is_active else "nonaktif"
        changes.append(f"status: {status}")

    if changes:
        log = Aktivitas(
            tipe="edit_user",
            deskripsi=f"Admin mengubah user {user.username}: {', '.join(changes)}",
            user_id=admin.id,
            target_user_id=user.id,
        )
        db.add(log)
        db.commit()

    return updated


@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), admin=Depends(require_admin)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")
    if user.id == admin.id:
        raise HTTPException(status_code=400, detail="Tidak dapat menghapus akun sendiri")

    username = user.username
    db.delete(user)

    # Log aktivitas
    log = Aktivitas(
        tipe="hapus_user",
        deskripsi=f"Admin menghapus user: {username}",
        user_id=admin.id,
    )
    db.add(log)
    db.commit()

    return {"message": f"User {username} berhasil dihapus"}


@router.post("/users/{user_id}/deactivate")
def nonaktif_user(user_id: int, db: Session = Depends(get_db), admin=Depends(require_admin)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")
    if user.id == admin.id:
        raise HTTPException(status_code=400, detail="Tidak dapat menonaktifkan akun sendiri")

    updated = deactivate_user(db, user_id)

    # Log aktivitas
    log = Aktivitas(
        tipe="nonaktif_user",
        deskripsi=f"Admin menonaktifkan user: {user.username}",
        user_id=admin.id,
        target_user_id=user.id,
    )
    db.add(log)
    db.commit()

    return {"message": f"User {user.username} berhasil dinonaktifkan"}
