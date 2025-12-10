from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Person(Base):
    """Abstract Base Class (Inheritance) for common attributes"""
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def get_summary(self):
        """Polymorphism: method to be overridden or used as is"""
        return f"{self.nama} ({self.email})"

class User(Person):
    """User/Admin for Authentication"""
    __tablename__ = "users"
    
    hashed_password = Column(String)
    
    def get_summary(self): # Polymorphism
        return f"Admin: {self.nama}"

class Student(Person):
    """Student Data"""
    __tablename__ = "students"
    
    nim = Column(String, unique=True, index=True) # ID Mahasiswa
    jurusan = Column(String)
    ipk = Column(Float)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Encapsulation could be simulated by properties or validation in logic layer
    
    def get_summary(self): # Polymorphism
        return f"Mahasiswa: {self.nama} [{self.nim}]"
