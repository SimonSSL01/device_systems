from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class UserBase(BaseModel):
    name: str = Field(..., min_length=3, description="Nombre completo")
    email: EmailStr = Field(..., description="Correo electrónico válido")
    role: str = Field(..., description="Rol del usuario: admin, support, user")
    is_active: bool = Field(default=True, description="Estado del usuario")

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int