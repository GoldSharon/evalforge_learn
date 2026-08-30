from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class DatasetCreate(BaseModel):
    name: str 
    description: str 


class DatasetResponse(BaseModel):
    id: str 
    name: str 
    description: Optional[str] = None 
    created_at : datetime

    class Config:
        from_attributes = True

class DatasetUpdate(BaseModel):
    name: Optional[str] = None 
    description: Optional[str] = None

class UserCreate(BaseModel):
    email: str
    full_name: str | None = None 
    password: str 

class UserResponse(BaseModel):
    id:str 
    email: str
    full_name: str | None = None 
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True