from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.device_model import Device
from app.models.loan_model import Loan  
from app.schemas.device_schema import DeviceCreate, DeviceUpdate, DevicePatch

def get_all_devices(db: Session, device_type: str = None, is_available: bool = None, brand: str = None, search: str = None):
    query = db.query(Device)
    if device_type:
        query = query.filter(Device.device_type == device_type)
    if is_available is not None:
        query = query.filter(Device.is_available == is_available)
    if brand:
        query = query.filter(Device.brand.ilike(f"%{brand}%"))
    if search:
        query = query.filter(
            Device.name.ilike(f"%{search}%") | Device.serial_number.ilike(f"%{search}%")
        )
    return query.all()

def get_device_by_id(db: Session, device_id: int):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    return device

def create_device(db: Session, device_data: DeviceCreate):
    existing = db.query(Device).filter(Device.serial_number == device_data.serial_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="El número de serie ya está registrado")
    allowed_types = ["laptop", "tablet", "projector", "camera", "router", "monitor"]
    if device_data.device_type.lower() not in allowed_types:
        raise HTTPException(status_code=400, detail=f"Tipo no permitido. Tipos: {', '.join(allowed_types)}")
    
    new_device = Device(**device_data.dict())
    db.add(new_device)
    db.commit()
    db.refresh(new_device)
    return new_device

def update_device(db: Session, device_id: int, device_update: DeviceUpdate):
    device = get_device_by_id(db, device_id)
    if device_update.serial_number != device.serial_number:
        existing = db.query(Device).filter(Device.serial_number == device_update.serial_number).first()
        if existing:
            raise HTTPException(status_code=400, detail="El número de serie ya está registrado")
    for key, value in device_update.dict().items():
        setattr(device, key, value)
    db.commit()
    db.refresh(device)
    return device

def patch_device(db: Session, device_id: int, device_patch: DevicePatch):
    device = get_device_by_id(db, device_id)
    update_data = device_patch.dict(exclude_unset=True)
    if "serial_number" in update_data and update_data["serial_number"] != device.serial_number:
        existing = db.query(Device).filter(Device.serial_number == update_data["serial_number"]).first()
        if existing:
            raise HTTPException(status_code=400, detail="El número de serie ya está registrado")
    for key, value in update_data.items():
        setattr(device, key, value)
    db.commit()
    db.refresh(device)
    return device

def delete_device(db: Session, device_id: int):
    device = get_device_by_id(db, device_id)
    active_loans = db.query(Loan).filter(Loan.device_id == device_id, Loan.status == "active").first()
    if active_loans:
        raise HTTPException(status_code=400, detail="No se puede eliminar un dispositivo con préstamos activos")
    db.delete(device)
    db.commit()
    return {"message": "Dispositivo eliminado correctamente"}