from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import Optional, List
from app.schemas.user_schema import UserCreate, UserResponse, UserUpdate, UserPatch
from app.services import user_service
from app.database.connection import get_db
from app.dependencies.user_dependencies import verify_headers   # dependencia de cabeceras (opcional)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(verify_headers)]   # si quieres mantener la validación de cabeceras
)

@router.get("/", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
async def get_users(
    role: Optional[str] = Query(None, description="Filtrar por rol (admin, support, user)"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo/inactivo"),
    db: Session = Depends(get_db)
):
    return user_service.get_all_users(db, role, is_active)

@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    return user_service.get_user_by_id(db, user_id)

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, user)

@router.put("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    return user_service.update_user(db, user_id, user)

@router.patch("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def patch_user(user_id: int, user_patch: UserPatch, db: Session = Depends(get_db)):
    return user_service.patch_user(db, user_id, user_patch)

@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    return user_service.delete_user(db, user_id)