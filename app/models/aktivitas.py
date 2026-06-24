from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Aktivitas(Base):
    __tablename__ = "aktivitas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    perangkat_id = Column(Integer, ForeignKey("perangkat.id"), nullable=False)
    tipe = Column(String(30), nullable=False)
    deskripsi = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    cabang_asal_id = Column(Integer, ForeignKey("cabang.id"))
    cabang_tujuan_id = Column(Integer, ForeignKey("cabang.id"))
    peminjam = Column(String(100))
    status_sebelumnya = Column(String(20))
    status_baru = Column(String(20))
    created_at = Column(DateTime, server_default=func.now())

    perangkat = relationship("Perangkat")
    user = relationship("User")
