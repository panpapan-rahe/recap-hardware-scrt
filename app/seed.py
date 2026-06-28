from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.cabang import Cabang
from app.models.kategori import Kategori
from app.services.auth_service import hash_password


def seed():
    db = next(get_db())
    try:
        # Seed admin user (default)
        if not db.query(User).filter(User.username == "admin").first():
            admin = User(
                username="admin",
                password_hash=hash_password("admin"),
                nama_lengkap="Administrator",
                role="admin",
            )
            db.add(admin)
            print("✅ Admin user (admin / admin)")

        # Seed kategori default
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
