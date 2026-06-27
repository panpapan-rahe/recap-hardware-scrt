from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Cabang(Base):
    __tablename__ = "cabang"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    kode = Column(String(10), unique=True, nullable=False)
    inisial = Column(String(10))
    nama = Column(String(100), nullable=False)
    alamat = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
