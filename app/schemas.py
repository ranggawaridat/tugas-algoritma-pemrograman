from pydantic import BaseModel, EmailStr, field_validator
import re
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    nama: str

class UserLogin(BaseModel):
    username: str
    password: str

class StudentBase(BaseModel):
    nama: str
    email: EmailStr
    nim: str
    jurusan: str
    ipk: float

    @field_validator('nim')
    def validate_nim(cls, v):
        if not re.match(r'^\d+$', v):
            raise ValueError('NIM must contain only numbers')
        return v

    @field_validator('nama')
    def validate_nama(cls, v):
        if not re.match(r"^[a-zA-Z\s\.]+$", v):
            raise ValueError('Name must contain only letters, spaces, or dots')
        return v
    
    @field_validator('ipk')
    def validate_ipk(cls, v):
        if v < 0.0 or v > 4.0:
            raise ValueError('IPK must be between 0.00 and 4.00')
        return v

class StudentCreate(StudentBase):
    pass

class StudentUpdate(StudentBase):
    pass

class StudentResponse(StudentBase):
    id: int
    
    class Config:
        from_attributes = True
