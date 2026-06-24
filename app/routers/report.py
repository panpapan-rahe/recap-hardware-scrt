from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.deps import get_current_user_id
from app.services.report_service import get_report_data, generate_csv, generate_pdf

router = APIRouter(prefix="/report", tags=["Report"])


@router.get("/data")
def report_data(
    cabang_id: int = Query(None),
    kategori_id: int = Query(None),
    status: str = Query(None),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    data = get_report_data(db, cabang_id, kategori_id, status)
    return {
        "total": len(data),
        "data": [
            {
                "id": d.id,
                "kode_unik": d.kode_unik,
                "nama": d.nama,
                "kategori": d.kategori.nama if d.kategori else "-",
                "merk": d.merk,
                "model": d.model,
                "serial_number": d.serial_number,
                "tahun_beli": d.tahun_beli,
                "cabang": d.cabang.nama if d.cabang else "-",
                "lokasi_detail": d.lokasi_detail,
                "status": d.status,
            }
            for d in data
        ],
    }


@router.get("/export/csv")
def export_csv(
    cabang_id: int = Query(None),
    kategori_id: int = Query(None),
    status: str = Query(None),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    data = get_report_data(db, cabang_id, kategori_id, status)
    csv_content = generate_csv(data)
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=report_perangkat.csv"},
    )


@router.get("/export/pdf")
def export_pdf(
    cabang_id: int = Query(None),
    kategori_id: int = Query(None),
    status: str = Query(None),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    data = get_report_data(db, cabang_id, kategori_id, status)
    title = "Report Perangkat IT"
    if status:
        title += f" - Status: {status}"
    pdf_bytes = generate_pdf(data, title)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=report_perangkat.pdf"},
    )
