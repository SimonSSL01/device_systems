from pydantic import BaseModel, Field, EmailStr
from typing import Optional

# Base (común)
class UserBase(BaseModel):
    name: str = Field(..., min_length=3)
    email: EmailStr
    role: str = Field(..., description="admin, support, user")
    is_active: bool = True

# Para creación (igual a Base)
class UserCreate(UserBase):
    pass

# Para respuesta (incluye id)
class UserResponse(UserBase):
    id: int

# Para actualización completa (PUT)
class UserUpdate(UserBase):
    pass

# Para actualización parcial (PATCH) - todos opcionales
class UserPatch(BaseModel):
    name: Optional[str] = Field(None, min_length=3)
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None