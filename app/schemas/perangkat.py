from pydantic import BaseModel
from typing import Optional


class PerangkatCreate(BaseModel):
    kategori_id: Optional[int] = None
    cabang_id: int
    merk: Optional[str] = None
    model: Optional[str] = None  # dipakai sebagai "Type" di UI
    adjuro: Optional[str] = None
    serial_number: Optional[str] = None
    tahun_beli: Optional[int] = None
    status: Optional[str] = "aktif"
    lokasi_detail: Optional[str] = None


class PerangkatUpdate(BaseModel):
    kategori_id: Optional[int] = None
    cabang_id: Optional[int] = None
    merk: Optional[str] = None
    model: Optional[str] = None  # dipakai sebagai "Type" di UI
    adjuro: Optional[str] = None
    serial_number: Optional[str] = None
    tahun_beli: Optional[int] = None
    status: Optional[str] = None
    lokasi_detail: Optional[str] = None


class PerangkatResponse(BaseModel):
    id: int
    kode_unik: str
    nama: str
    kategori_id: Optional[int] = None
    kategori_nama: Optional[str] = None
    cabang_id: int
    merk: Optional[str] = None
    model: Optional[str] = None
    adjuro: Optional[str] = None
    serial_number: Optional[str] = None
    tahun_beli: Optional[int] = None
    status: Optional[str] = None
    lokasi_detail: Optional[str] = None

    class Config:
        from_attributes = True


class PerangkatDetail(PerangkatResponse):
    kategori_nama: Optional[str] = None
    cabang_nama: str
    cabang_kode: str


# FASE 2: Aktivitas schemas
class PindahRequest(BaseModel):
    cabang_tujuan_id: int
    deskripsi: Optional[str] = None


class PinjamRequest(BaseModel):
    peminjam: str
    deskripsi: Optional[str] = None


class MaintenanceRequest(BaseModel):
    deskripsi: Optional[str] = None
