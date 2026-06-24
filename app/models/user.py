from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    nama_lengkap = Column(String(100), nullable=False)
    role = Column(String(20), default="viewer")
    created_at = Column(DateTime, server_default=func.now())
