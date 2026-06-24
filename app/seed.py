import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine, Base
from app.models import User, Cabang, Kategori
from app.services.auth_service import hash_password


def seed():
    db = SessionLocal()
    try:
        # Buat user admin
        if not db.query(User).filter(User.username == "admin").first():
            admin = User(
                username="admin",
                password_hash=hash_password("admin123"),
                nama_lengkap="Administrator",
                role="admin",
            )
            db.add(admin)
            print("✅ Admin user created: admin / admin123")

        # Buat sample cabang
        cabang_data = [
            {"kode": "BR01", "nama": "Cabang Pusat", "alamat": "Jl. Raya No. 1"},
            {"kode": "BR02", "nama": "Cabang Utara", "alamat": "Jl. Utara No. 10"},
            {"kode": "BR03", "nama": "Cabang Selatan", "alamat": "Jl. Selatan No. 5"},
            {"kode": "BR04", "nama": "Cabang Timur", "alamat": "Jl. Timur No. 8"},
        ]
        for data in cabang_data:
            if not db.query(Cabang).filter(Cabang.kode == data["kode"]).first():
                db.add(Cabang(**data))
                print(f"✅ Cabang {data['kode']} - {data['nama']}")

        # Buat sample kategori
        kategori_data = [
            {"nama": "Laptop", "deskripsi": "Laptop & Notebook"},
            {"nama": "PC Desktop", "deskripsi": "PC Tower / Desktop"},
            {"nama": "Printer", "deskripsi": "Printer & Scanner"},
            {"nama": "Router", "deskripsi": "Router & Access Point"},
            {"nama": "Switch", "deskripsi": "Network Switch"},
            {"nama": "POS", "deskripsi": "Mesin POS & Peripheral"},
        ]
        for data in kategori_data:
            if not db.query(Kategori).filter(Kategori.nama == data["nama"]).first():
                db.add(Kategori(**data))
                print(f"✅ Kategori {data['nama']}")

        db.commit()
        print("\n🎉 Seed data selesai!")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
