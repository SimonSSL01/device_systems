from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class DeviceBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    serial_number: str = Field(..., min_length=5)
    device_type: str = Field(..., description="laptop, tablet, projector, camera, router, monitor")
    brand: Optional[str] = Field(None, max_length=50)
    is_available: bool = True

class DeviceCreate(DeviceBase):
    pass

class DeviceUpdate(DeviceBase):
    pass

class DevicePatch(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    serial_number: Optional[str] = Field(None, min_length=5)
    device_type: Optional[str] = None
    brand: Optional[str] = Field(None, max_length=50)
    is_available: Optional[bool] = None

class DeviceResponse(DeviceBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)