from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.auth.security import decode_access_token
from app.auth.auth_service import get_user_by_email

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    email = payload.get("sub")
    if email is None:
        raise HTTPException(status_code=401, detail="Token inválido")
    user = get_user_by_email(db, email)
    if user is None:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return user

def get_current_active_user(current_user = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="Usuario inactivo")
    return current_user

def require_admin(current_user = Depends(get_current_active_user)):
    if current_user.role not in ["admin", "support"]:
        raise HTTPException(status_code=403, detail="No tienes permisos suficientes")
    return current_user

def require_admin_only(current_user = Depends(get_current_active_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Se requiere rol administrador")
    return current_user