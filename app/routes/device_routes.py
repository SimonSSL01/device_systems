from fastapi import APIRouter, Depends, Query, status, Request
from sqlalchemy.orm import Session
from typing import Optional, List
from app.schemas.device_schema import DeviceCreate, DeviceUpdate, DevicePatch, DeviceResponse
from app.services import device_service
from app.database.connection import get_db
from app.dependencies.auth_dependency import require_admin, require_admin_only
from app.limiter import limiter
from fastapi import Request

router = APIRouter(
    prefix="/devices",
    tags=["Devices"]
)

@router.get("/", response_model=List[DeviceResponse], status_code=status.HTTP_200_OK)
async def get_devices(
    device_type: Optional[str] = Query(None, description="Filtrar por tipo (laptop, tablet, etc.)"),
    is_available: Optional[bool] = Query(None, description="Filtrar por disponibilidad"),
    brand: Optional[str] = Query(None, description="Filtrar por marca (búsqueda parcial)"),
    search: Optional[str] = Query(None, description="Buscar por nombre o número de serie"),
    db: Session = Depends(get_db)
    # Público: no requiere autenticación
):
    return device_service.get_all_devices(db, device_type, is_available, brand, search)

@router.get("/{device_id}", response_model=DeviceResponse, status_code=status.HTTP_200_OK)
async def get_device(
    device_id: int,
    db: Session = Depends(get_db)
    # Público: no requiere autenticación
):
    return device_service.get_device_by_id(db, device_id)

@router.post("/", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED)
async def create_device(
    device: DeviceCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)  # Protección: admin o support
):
    return device_service.create_device(db, device)

@router.put("/{device_id}", response_model=DeviceResponse, status_code=status.HTTP_200_OK)
async def update_device(
    device_id: int,
    device: DeviceUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)  # Protección: admin o support
):
    return device_service.update_device(db, device_id, device)

@router.patch("/{device_id}", response_model=DeviceResponse, status_code=status.HTTP_200_OK)
async def patch_device(
    device_id: int,
    device_patch: DevicePatch,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)  # Protección: admin o support
):
    return device_service.patch_device(db, device_id, device_patch)

@router.delete("/{device_id}", status_code=status.HTTP_200_OK)
async def delete_device(
    device_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin_only)  # Protección: solo admin
):
    return device_service.delete_device(db, device_id)