from fastapi import APIRouter, Depends, Query, status, Request  # <-- AÑADIR Request
from sqlalchemy.orm import Session
from typing import Optional, List
from app.schemas.loan_schema import LoanCreate, LoanResponse, LoanDetailResponse
from app.services import loan_service
from app.database.connection import get_db
from app.dependencies.auth_dependency import get_current_active_user, require_admin
from app.limiter import limiter

router = APIRouter(
    prefix="/loans",
    tags=["Loans"]
)

@router.get("/details", response_model=List[LoanDetailResponse], status_code=status.HTTP_200_OK)
async def get_loans_details(
    status: Optional[str] = Query(None, description="Filtrar por estado"),
    user_email: Optional[str] = Query(None, description="Filtrar por email del usuario"),
    device_type: Optional[str] = Query(None, description="Filtrar por tipo de dispositivo"),
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    loans = loan_service.get_loans_with_details(db, status, user_email, device_type)
    result = []
    for loan in loans:
        result.append({
            "loan_id": loan.id,
            "status": loan.status,
            "loan_date": loan.loan_date,
            "return_date": loan.return_date,
            "user": {
                "id": loan.user.id,
                "name": loan.user.name,
                "email": loan.user.email
            },
            "device": {
                "id": loan.device.id,
                "name": loan.device.name,
                "serial_number": loan.device.serial_number,
                "device_type": loan.device.device_type
            }
        })
    return result

@router.get("/user/{user_id}", response_model=List[LoanResponse], status_code=status.HTTP_200_OK)
async def get_loans_by_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    return loan_service.get_loans_by_user(db, user_id)

@router.get("/device/{device_id}", response_model=List[LoanResponse], status_code=status.HTTP_200_OK)
async def get_loans_by_device(
    device_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    return loan_service.get_loans_by_device(db, device_id)

@router.get("/{loan_id}", response_model=LoanResponse, status_code=status.HTTP_200_OK)
async def get_loan(
    loan_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    return loan_service.get_loan_by_id(db, loan_id)

@router.get("/", response_model=List[LoanResponse], status_code=status.HTTP_200_OK)
@limiter.limit("30/minute")
async def get_loans(
    request: Request,
    status: Optional[str] = Query(None, description="Filtrar por estado (active, returned, overdue)"),
    user_id: Optional[int] = Query(None, description="Filtrar por ID de usuario"),
    device_id: Optional[int] = Query(None, description="Filtrar por ID de dispositivo"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    return loan_service.get_all_loans(db, status, user_id, device_id)

@router.post("/", response_model=LoanResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
async def create_loan(
    request: Request, 
    loan: LoanCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    return loan_service.create_loan(db, loan)

@router.patch("/{loan_id}/return", response_model=LoanResponse, status_code=status.HTTP_200_OK)
async def return_loan(
    loan_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    return loan_service.return_loan(db, loan_id)

@router.delete("/{loan_id}", status_code=status.HTTP_200_OK)
async def delete_loan(
    loan_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    return loan_service.delete_loan(db, loan_id)