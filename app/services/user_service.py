from app.data.user_db import fake_db, get_next_id
from app.schemas.user_schema import UserCreate, UserUpdate, UserPatch
from fastapi import HTTPException, status

def get_all_users(role: str = None, is_active: bool = None):
    result = fake_db
    if role:
        result = [u for u in result if u["role"] == role]
    if is_active is not None:
        result = [u for u in result if u["is_active"] == is_active]
    return result

def get_user_by_id(user_id: int):
    user = next((u for u in fake_db if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

def create_user(user_data: UserCreate):
    # Verificar email duplicado
    if any(u["email"] == user_data.email for u in fake_db):
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    if user_data.role not in ["admin", "support", "user"]:
        raise HTTPException(status_code=400, detail="Rol no permitido")
    
    new_user = user_data.dict()
    new_user["id"] = get_next_id()
    fake_db.append(new_user)
    return new_user

def update_user(user_id: int, user_update: UserUpdate):
    user = get_user_by_id(user_id)
    # Verificar email duplicado (si cambia)
    if user_update.email != user["email"] and any(u["email"] == user_update.email for u in fake_db):
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    if user_update.role not in ["admin", "support", "user"]:
        raise HTTPException(status_code=400, detail="Rol no permitido")
    
    # Actualizar campos
    user.update(user_update.dict())
    return user

def patch_user(user_id: int, user_patch: UserPatch):
    user = get_user_by_id(user_id)
    update_data = user_patch.dict(exclude_unset=True)
    
    # Validar email si se envía
    if "email" in update_data and update_data["email"] != user["email"]:
        if any(u["email"] == update_data["email"] for u in fake_db):
            raise HTTPException(status_code=400, detail="El correo ya está registrado")
    
    # Validar rol si se envía
    if "role" in update_data and update_data["role"] not in ["admin", "support", "user"]:
        raise HTTPException(status_code=400, detail="Rol no permitido")
    
    user.update(update_data)
    return user

def delete_user(user_id: int):
    user = get_user_by_id(user_id)
    fake_db.remove(user)
    return {"message": "Usuario eliminado correctamente"}