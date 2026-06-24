from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Kategori(Base):
    __tablename__ = "kategori"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nama = Column(String(50), nullable=False)
    deskripsi = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
