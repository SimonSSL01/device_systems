from fastapi import APIRouter, Depends, Query, status
from typing import Optional, List
from app.schemas.user_schema import UserCreate, UserResponse, UserUpdate, UserPatch
from app.services import user_service
from app.dependencies.user_dependencies import verify_headers

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(verify_headers)]
)

@router.get(
    "/",
    response_model=List[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar usuarios",
    description="Obtiene todos los usuarios. Puede filtrar por rol y estado activo."
)
async def get_users(
    role: Optional[str] = Query(None, description="Filtrar por rol (admin, support, user)"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo/inactivo")
):
    return user_service.get_all_users(role, is_active)

@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener usuario por ID",
    description="Retorna un usuario específico según su ID."
)
async def get_user(user_id: int):
    return user_service.get_user_by_id(user_id)

@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear usuario",
    description="Registra un nuevo usuario. Valida email único y rol permitido."
)
async def create_user(user: UserCreate):
    return user_service.create_user(user)

@router.put(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar usuario completamente",
    description="Reemplaza todos los datos del usuario (requiere todos los campos)."
)
async def update_user(user_id: int, user: UserUpdate):
    return user_service.update_user(user_id, user)

@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar usuario parcialmente",
    description="Actualiza solo los campos enviados en la petición."
)
async def patch_user(user_id: int, user_patch: UserPatch):
    return user_service.patch_user(user_id, user_patch)

@router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,   # O también 204 sin cuerpo
    summary="Eliminar usuario",
    description="Borra un usuario de la base de datos."
)
async def delete_user(user_id: int):
    return user_service.delete_user(user_id)