from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserUpdate, UserPatch

# Obtener todos los usuarios (con filtros opcionales)
def get_all_users(db: Session, role: str = None, is_active: bool = None):
    query = db.query(User)
    if role:
        query = query.filter(User.role == role)
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    return query.all()

# Obtener un usuario por ID (lanza 404 si no existe)
def get_user_by_id(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

# Crear usuario (valida email único y rol permitido)
def create_user(db: Session, user_data: UserCreate):
    # Validar rol
    if user_data.role not in ["admin", "support", "user"]:
        raise HTTPException(status_code=400, detail="Rol no permitido")
    # Validar email único
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        role=user_data.role,
        is_active=user_data.is_active
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Actualizar completamente (PUT)
def update_user(db: Session, user_id: int, user_update: UserUpdate):
    user = get_user_by_id(db, user_id)
    # Validar rol
    if user_update.role not in ["admin", "support", "user"]:
        raise HTTPException(status_code=400, detail="Rol no permitido")
    # Si el email cambió, verificar que no exista ya en otro usuario
    if user_update.email != user.email:
        existing = db.query(User).filter(User.email == user_update.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="El correo ya está registrado")
    
    user.name = user_update.name
    user.email = user_update.email
    user.role = user_update.role
    user.is_active = user_update.is_active
    db.commit()
    db.refresh(user)
    return user

# Actualizar parcialmente (PATCH)
def patch_user(db: Session, user_id: int, user_patch: UserPatch):
    user = get_user_by_id(db, user_id)
    update_data = user_patch.dict(exclude_unset=True)
    
    # Validar email si se envía
    if "email" in update_data and update_data["email"] != user.email:
        existing = db.query(User).filter(User.email == update_data["email"]).first()
        if existing:
            raise HTTPException(status_code=400, detail="El correo ya está registrado")
    # Validar rol si se envía
    if "role" in update_data and update_data["role"] not in ["admin", "support", "user"]:
        raise HTTPException(status_code=400, detail="Rol no permitido")
    
    for key, value in update_data.items():
        setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    return user

# Eliminar usuario
def delete_user(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    db.delete(user)
    db.commit()
    return {"message": "Usuario eliminado correctamente"}