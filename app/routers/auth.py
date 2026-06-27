from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.services.auth_service import (
    authenticate_user, create_user, create_access_token, get_user_by_id,
)
from app.deps import get_current_user

router = APIRouter(tags=["Auth"])


@router.post("/register", response_model=UserResponse)
def register(data: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(status_code=400, detail="Username sudah terdaftar")
    return create_user(db, data.username, data.password, data.nama_lengkap, data.role)


@router.post("/login", response_model=Token)
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, data.username, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Username atau password salah")
    token = create_access_token({"sub": str(user.id), "username": user.username, "role": user.role})
    return {"access_token": token}


@router.get("/me", response_model=UserResponse)
def me(user: User = Depends(get_current_user)):
    return user
