from fastapi import APIRouter, Depends, status, Request, Form
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.auth_schema import UserRegister, UserLogin, Token, UserResponseAuth
from app.auth import auth_service
from app.dependencies.auth_dependency import get_current_active_user
from app.limiter import limiter
from fastapi import APIRouter, Depends, status, Request, Form, HTTPException

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/register", response_model=UserResponseAuth, status_code=status.HTTP_201_CREATED)
@limiter.limit("3/minute")
async def register(
    request: Request,
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    return auth_service.register_user(db, user_data)

@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
async def login(
    request: Request,
    username: str = Form(None), 
    password: str = Form(None), 
    user_login: UserLogin = None, 
    db: Session = Depends(get_db)
):
    if username is not None and password is not None:
        return auth_service.login_user(db, username, password)
    
    if user_login is not None:
        return auth_service.login_user(db, user_login.email, user_login.password)
    
    raise HTTPException(status_code=400, detail="Datos de login inválidos")

@router.get("/me", response_model=UserResponseAuth)
async def get_me(
    current_user = Depends(get_current_active_user)
):
    return current_user