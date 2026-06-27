from pydantic import BaseModel
from typing import Optional


class AktivitasBase(BaseModel):
    perangkat_id: int
    tipe: str
    deskripsi: Optional[str] = None
    cabang_asal_id: Optional[int] = None
    cabang_tujuan_id: Optional[int] = None
    peminjam: Optional[str] = None
    status_sebelumnya: Optional[str] = None
    status_baru: Optional[str] = None


class AktivitasCreate(AktivitasBase):
    pass


class AktivitasResponse(AktivitasBase):
    id: int
    user_id: int
    target_user_id: Optional[int] = None

    class Config:
        from_attributes = True
