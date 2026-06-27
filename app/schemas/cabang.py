from pydantic import BaseModel
from typing import Optional


class CabangBase(BaseModel):
    kode: str
    inisial: Optional[str] = None
    nama: str
    alamat: Optional[str] = None


class CabangCreate(CabangBase):
    pass


class CabangUpdate(BaseModel):
    kode: Optional[str] = None
    inisial: Optional[str] = None
    nama: Optional[str] = None
    alamat: Optional[str] = None


class CabangResponse(CabangBase):
    id: int

    class Config:
        from_attributes = True
