from fastapi import APIRouter, HTTPException, Header, Query
from typing import Optional, List
from app.schemas.user_schema import UserCreate, UserResponse

router = APIRouter()

# Base de datos simulada
fake_db = []
current_id = 1

@router.get("/users", response_model=List[UserResponse])
async def get_users(
    role: Optional[str] = Query(None, description="Filtrar por rol"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo/inactivo")
):
    """Lista todos los usuarios con filtros opcionales"""
    result = fake_db
    if role:
        result = [u for u in result if u["role"] == role]
    if is_active is not None:
        result = [u for u in result if u["is_active"] == is_active]
    return result

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    """Obtiene un usuario por su ID"""
    user = next((u for u in fake_db if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@router.post("/users", response_model=UserResponse, status_code=201)
async def create_user(
    user: UserCreate,
    x_app_name: str = Header(..., alias="X-App-Name"),
    x_api_version: str = Header(..., alias="X-API-Version")
):
    """Registra un nuevo usuario, evita correos duplicados y recibe cabeceras personalizadas"""
    global current_id
    
    # Verificar si el email ya existe
    if any(u["email"] == user.email for u in fake_db):
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    
    # Validar rol permitido
    if user.role not in ["admin", "support", "user"]:
        raise HTTPException(status_code=400, detail="Rol no permitido")
    
    new_user = user.dict()
    new_user["id"] = current_id
    fake_db.append(new_user)
    current_id += 1
    
    # Puedes usar las cabeceras para logging o validación adicional
    print(f"Aplicación: {x_app_name} - Versión: {x_api_version}")
    
    return new_user