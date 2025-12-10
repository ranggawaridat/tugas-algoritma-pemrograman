from sqlalchemy.orm import Session
from app import models, schemas
import csv
import io
from abc import ABC, abstractmethod
from typing import List

class DataManager(ABC):
    """Abstract Base Class for Data Management Business Logic"""
    
    def __init__(self, db: Session):
        self.db = db
    
    @abstractmethod
    def create(self, data):
        pass
    
    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, id, data):
        pass

    @abstractmethod
    def delete(self, id):
        pass

class StudentManager(DataManager):
    """Concrete implementation for Student Management"""
    
    def create(self, student: schemas.StudentCreate) -> models.Student:
        db_student = models.Student(
            nama=student.nama,
            email=student.email,
            nim=student.nim,
            jurusan=student.jurusan,
            ipk=student.ipk
        )
        self.db.add(db_student)
        try:
            self.db.commit()
            self.db.refresh(db_student)
        except Exception as e:
            self.db.rollback()
            raise e
        return db_student

    def get_all(self) -> List[models.Student]:
        return self.db.query(models.Student).all()
    
    def get_by_id(self, student_id: int):
        return self.db.query(models.Student).filter(models.Student.id == student_id).first()

    def update(self, student_id: int, student_data: schemas.StudentUpdate):
        db_student = self.get_by_id(student_id)
        if not db_student:
            from app.core.exceptions import DataNotFound
            raise DataNotFound(f"Student with ID {student_id} not found")
        
        # update fields
        for key, value in student_data.dict().items():
            setattr(db_student, key, value)
            
        self.db.commit()
        self.db.refresh(db_student)
        return db_student

    def delete(self, student_id: int):
        db_student = self.get_by_id(student_id)
        if not db_student:
             from app.core.exceptions import DataNotFound
             raise DataNotFound(f"Student with ID {student_id} not found")
             
        self.db.delete(db_student)
        self.db.commit()
        return True

    def export_csv(self) -> str:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['ID', 'NIM', 'Nama', 'Email', 'Jurusan', 'IPK'])
        
        students = self.get_all()
        for s in students:
            writer.writerow([s.id, s.nim, s.nama, s.email, s.jurusan, s.ipk])
            
        return output.getvalue()

    def import_csv(self, file_content: str):
        if not file_content.strip():
             from app.core.exceptions import FileEmpty
             raise FileEmpty()

        stream = io.StringIO(file_content)
        try:
            reader = csv.DictReader(stream)
            if not reader.fieldnames:
                 from app.core.exceptions import FileFormatError
                 raise FileFormatError("CSV Header missing")
                 
            count = 0
            for row in reader:
                # Basic validation/mapping
                try:
                    student_in = schemas.StudentCreate(
                        nama=row['Nama'],
                        email=row['Email'],
                        nim=row['NIM'],
                        jurusan=row['Jurusan'],
                        ipk=float(row['IPK'])
                    )
                    self.create(student_in)
                    count += 1
                except Exception as row_error:
                    # We might log this but continue or raise FormatError
                    # For strictness let's raise
                    from app.core.exceptions import FileFormatError
                    raise FileFormatError(f"Row error: {str(row_error)}")
            return count
        except csv.Error:
             from app.core.exceptions import FileFormatError
             raise FileFormatError("Invalid CSV format")
