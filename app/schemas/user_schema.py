from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

# Base con atributos comunes
class UserBase(BaseModel):
    name: str = Field(..., min_length=3, description="Nombre completo")
    email: EmailStr = Field(..., description="Correo electrónico válido")
    role: str = Field(..., description="Rol del usuario: admin, support, user")
    is_active: bool = Field(default=True, description="Usuario activo o inactivo")

# Para crear usuario (entrada)
class UserCreate(UserBase):
    pass

# Para actualizar completamente (PUT)
class UserUpdate(UserBase):
    pass

# Para actualización parcial (PATCH)
class UserPatch(BaseModel):
    name: Optional[str] = Field(None, min_length=3)
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None

# Para respuesta (incluye id y created_at)
class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # Permite convertir modelo SQLAlchemy a dict