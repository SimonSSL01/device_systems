from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class LoanBase(BaseModel):
    user_id: int
    device_id: int
    status: str = "active"

class LoanCreate(LoanBase):
    pass

class LoanUpdate(BaseModel):
    status: str
    return_date: Optional[datetime] = None

class LoanResponse(BaseModel):
    id: int
    user_id: int
    device_id: int
    loan_date: datetime
    return_date: Optional[datetime]
    status: str

    model_config = ConfigDict(from_attributes=True)

class LoanDetailResponse(BaseModel):
    loan_id: int
    status: str
    loan_date: datetime
    return_date: Optional[datetime]
    user: dict 
    device: dict 

    model_config = ConfigDict(from_attributes=True)

class UserBrief(BaseModel):
    id: int
    name: str
    email: str

class DeviceBrief(BaseModel):
    id: int
    name: str
    serial_number: str
    device_type: str