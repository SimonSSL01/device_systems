from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from app.models.loan_model import Loan
from app.models.user_model import User
from app.models.device_model import Device
from app.schemas.loan_schema import LoanCreate, LoanUpdate
from datetime import datetime

def get_all_loans(db: Session, status: str = None, user_id: int = None, device_id: int = None):
    query = db.query(Loan)
    if status:
        query = query.filter(Loan.status == status)
    if user_id:
        query = query.filter(Loan.user_id == user_id)
    if device_id:
        query = query.filter(Loan.device_id == device_id)
    return query.all()

def get_loan_by_id(db: Session, loan_id: int):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    return loan

def get_loans_with_details(db: Session, status: str = None, user_email: str = None, device_type: str = None):
    """Consulta con joins para obtener detalles de usuario y dispositivo"""
    query = db.query(Loan).join(User, Loan.user_id == User.id).join(Device, Loan.device_id == Device.id)
    if status:
        query = query.filter(Loan.status == status)
    if user_email:
        query = query.filter(User.email.ilike(f"%{user_email}%"))
    if device_type:
        query = query.filter(Device.device_type == device_type)
    return query.all()

def get_loans_by_user(db: Session, user_id: int):

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db.query(Loan).filter(Loan.user_id == user_id).all()

def get_loans_by_device(db: Session, device_id: int):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    return db.query(Loan).filter(Loan.device_id == device_id).all()

def create_loan(db: Session, loan_data: LoanCreate):

    user = db.query(User).filter(User.id == loan_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    device = db.query(Device).filter(Device.id == loan_data.device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")

    if not device.is_available:
        raise HTTPException(status_code=400, detail="El dispositivo no está disponible")
    
    new_loan = Loan(
        user_id=loan_data.user_id,
        device_id=loan_data.device_id,
        status="active"
    )
    db.add(new_loan)

    device.is_available = False
    db.commit()
    db.refresh(new_loan)
    return new_loan

def return_loan(db: Session, loan_id: int):
    loan = get_loan_by_id(db, loan_id)
    if loan.status == "returned":
        raise HTTPException(status_code=400, detail="El préstamo ya fue devuelto")

    loan.status = "returned"
    loan.return_date = datetime.now()

    device = db.query(Device).filter(Device.id == loan.device_id).first()
    if device:
        device.is_available = True
    db.commit()
    db.refresh(loan)
    return loan

def delete_loan(db: Session, loan_id: int):
    loan = get_loan_by_id(db, loan_id)
    if loan.status == "active":
        raise HTTPException(status_code=400, detail="No se puede eliminar un préstamo activo, debe devolverlo primero")
    db.delete(loan)
    db.commit()
    return {"message": "Préstamo eliminado correctamente"}