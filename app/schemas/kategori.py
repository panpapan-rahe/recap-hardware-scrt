from pydantic import BaseModel
from typing import Optional


class KategoriBase(BaseModel):
    nama: str
    deskripsi: Optional[str] = None


class KategoriCreate(KategoriBase):
    pass


class KategoriUpdate(BaseModel):
    nama: Optional[str] = None
    deskripsi: Optional[str] = None


class KategoriResponse(KategoriBase):
    id: int

    class Config:
        from_attributes = True
