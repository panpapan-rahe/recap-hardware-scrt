import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/db.sqlite3")
SECRET_KEY = os.getenv("SECRET_KEY", "***")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480  # 8 jam
