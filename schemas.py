from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class DatasetCreate(BaseModel):
    name: str 
    description: str 


class DatasetResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str 
    name: str 
    description: Optional[str] = None 
    created_at : datetime


class DatasetUpdate(BaseModel):
    name: Optional[str] = None 
    description: Optional[str] = None

class UserCreate(BaseModel):
    email: str
    full_name: str | None = None 
    password: str 

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)


    id:str 
    email: str
    full_name: str | None = None 
    is_active: bool
    created_at: datetime

