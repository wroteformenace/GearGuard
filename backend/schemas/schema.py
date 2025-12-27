from pydantic import BaseModel, Field
import uuid
from datetime import datetime

class UserCreateSchema(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str
    password: str
    role: str

class UserLoginSchema(BaseModel):
    email: str
    password: str

class UserResponseSchema(BaseModel):
    uid: str
    username: str
    email: str
    first_name: str
    last_name: str
    password_hash: str = Field(exclude=True)
    role: str
    created_at: datetime
    updated_at: datetime

class EquipmentCreateSchema(BaseModel):
    name: str = Field(min_length=1 , max_length=100) 
    serial_number: str
    location: str
    isScrapped: bool = False

class EquipmentCategoryCreateSchema(BaseModel):
    name: str = Field(min_length=1 , max_length=100)

class EquipmentCategoryUpdateSchema(BaseModel):
    name: str = Field(min_length=1 , max_length=100)

class MaintenanceCreateSchema(BaseModel):
    name: str = Field(min_length=1 , max_length=100)