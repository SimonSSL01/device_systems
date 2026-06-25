from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator
from typing import Optional
from datetime import datetime 

class UserRegister(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    role: str = Field(default="user")

    @field_validator('password')
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('La contraseña debe tener al menos una mayúscula')
        if not any(c.islower() for c in v):
            raise ValueError('La contraseña debe tener al menos una minúscula')
        if not any(c.isdigit() for c in v):
            raise ValueError('La contraseña debe tener al menos un número')
        if ' ' in v:
            raise ValueError('La contraseña no puede contener espacios')
        return v

    @field_validator('role')
    def validate_role(cls, v):
        if v not in ["admin", "support", "user"]:
            raise ValueError('Rol no permitido. Debe ser admin, support o user')
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None

class UserResponseAuth(BaseModel):
    id: int
    name: str
    email: str
    role: str
    is_active: bool
    created_at: datetime  

    model_config = ConfigDict(from_attributes=True)