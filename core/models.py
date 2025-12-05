import re
from pydantic import BaseModel, field_validator, Field
from typing import Optional

# Konsep OOP: Class dan Enkapsulasi
class Mahasiswa(BaseModel):
    nim: str = Field(..., description="Nomor Induk Mahasiswa")
    nama: str = Field(..., description="Nama Lengkap")
    jurusan: str = Field(..., description="Jurusan")
    ipk: float = Field(..., ge=0.0, le=4.0, description="Indeks Prestasi Kumulatif")

    # Validasi Input menggunakan Regex (NIM harus angka)
    @field_validator('nim')
    def validate_nim(cls, v):
        if not re.match(r'^\d+$', v):
            raise ValueError('NIM harus berupa angka')
        return v

    # Validasi Nama (Hanya huruf dan spasi)
    @field_validator('nama')
    def validate_nama(cls, v):
        if not re.match(r'^[a-zA-Z\s]+$', v):
            raise ValueError('Nama hanya boleh berisi huruf dan spasi')
        return v
