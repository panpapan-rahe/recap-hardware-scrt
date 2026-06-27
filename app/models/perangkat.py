from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Perangkat(Base):
    __tablename__ = "perangkat"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    kode_unik = Column(String(20), unique=True, nullable=False)
    nama = Column(String(100), nullable=False)
    kategori_id = Column(Integer, ForeignKey("kategori.id"), nullable=False)
    merk = Column(String(50))
    model = Column(String(50))
    adjuro = Column(String(100))
    serial_number = Column(String(100))
    tahun_beli = Column(Integer)
    status = Column(String(20), default="aktif")
    cabang_id = Column(Integer, ForeignKey("cabang.id"), nullable=False)
    lokasi_detail = Column(String(200))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    kategori = relationship("Kategori")
    cabang = relationship("Cabang")
