from pydantic import BaseModel
from typing import Optional


class PerangkatBase(BaseModel):
    nama: str
    kategori_id: int
    merk: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    tahun_beli: Optional[int] = None
    status: Optional[str] = "aktif"
    cabang_id: int
    lokasi_detail: Optional[str] = None


class PerangkatCreate(PerangkatBase):
    pass


class PerangkatUpdate(BaseModel):
    nama: Optional[str] = None
    kategori_id: Optional[int] = None
    merk: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    tahun_beli: Optional[int] = None
    status: Optional[str] = None
    cabang_id: Optional[int] = None
    lokasi_detail: Optional[str] = None


class PerangkatResponse(PerangkatBase):
    id: int
    kode_unik: str

    class Config:
        from_attributes = True


class PerangkatDetail(PerangkatResponse):
    kategori_nama: str
    cabang_nama: str
    cabang_kode: str
