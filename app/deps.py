from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.services.auth_service import decode_token, get_user_by_id
from app.database import get_db

security = HTTPBearer()


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> int:
    try:
        payload = decode_token(credentials.credentials)
        user_id = int(payload.get("sub"))
        user = get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=401, detail="User tidak ditemukan")
        return user_id
    except Exception:
        raise HTTPException(status_code=401, detail="Token tidak valid")
