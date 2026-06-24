from sqlalchemy.orm import Session
from fpdf import FPDF
from datetime import datetime
from app.models.perangkat import Perangkat
from app.models.aktivitas import Aktivitas


def get_report_data(db: Session, cabang_id: int = None, kategori_id: int = None, status: str = None):
    query = db.query(Perangkat)
    if cabang_id:
        query = query.filter(Perangkat.cabang_id == cabang_id)
    if kategori_id:
        query = query.filter(Perangkat.kategori_id == kategori_id)
    if status:
        query = query.filter(Perangkat.status == status)
    return query.order_by(Perangkat.cabang_id, Perangkat.kode_unik).all()


def generate_csv(data: list) -> str:
    lines = ["Kode Unik,Nama,Kategori,Merk,Model,Serial Number,Tahun Beli,Cabang,Lokasi,Status"]
    for item in data:
        kategori = item.kategori.nama if item.kategori else "-"
        cabang = item.cabang.nama if item.cabang else "-"
        lines.append(
            f"{item.kode_unik},{item.nama},{kategori},{item.merk or '-'},{item.model or '-'},"
            f"{item.serial_number or '-'},{item.tahun_beli or '-'},{cabang},{item.lokasi_detail or '-'},{item.status}"
        )
    return "\n".join(lines)


def generate_pdf(data: list, title: str = "Report Perangkat IT") -> bytes:
    pdf = FPDF()
    pdf.add_page("L")  # Landscape
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, title, ln=True, align="C")
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 8, f"Tanggal: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align="C")
    pdf.ln(5)

    # Header
    headers = ["Kode", "Nama", "Kategori", "Merk/Model", "Cabang", "Status"]
    col_widths = [30, 50, 35, 45, 40, 25]
    pdf.set_font("Arial", "B", 9)
    for i, h in enumerate(headers):
        pdf.cell(col_widths[i], 8, h, 1)
    pdf.ln()

    # Data
    pdf.set_font("Arial", "", 8)
    for item in data:
        kategori = item.kategori.nama if item.kategori else "-"
        cabang = item.cabang.nama if item.cabang else "-"
        merk_model = f"{item.merk or ''} {item.model or ''}".strip()
        row = [item.kode_unik, item.nama, kategori, merk_model, cabang, item.status]
        for i, val in enumerate(row):
            pdf.cell(col_widths[i], 7, str(val)[:25], 1)
        pdf.ln()

    return bytes(pdf.output())
