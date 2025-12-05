import json
import os
from typing import List, Optional
from .models import Mahasiswa
from .algorithms import SortingAlgorithms, SearchingAlgorithms

DATA_FILE = "data/mahasiswa.json"

class ManajemenMahasiswa:
    def __init__(self):
        self.mahasiswa_list: List[Mahasiswa] = []
        self.load_data()

    # File I/O: Membaca data dari file JSON
    def load_data(self):
        if not os.path.exists(DATA_FILE):
            self.mahasiswa_list = []
            return

        try:
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
                # Konversi dict ke objek Mahasiswa
                self.mahasiswa_list = [Mahasiswa(**item) for item in data]
        except (json.JSONDecodeError, FileNotFoundError):
            self.mahasiswa_list = []
        except Exception as e:
            print(f"Error loading data: {e}")
            self.mahasiswa_list = []

    # File I/O: Menyimpan data ke file JSON
    def save_data(self):
        try:
            # Pastikan direktori ada
            os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
            
            with open(DATA_FILE, 'w') as f:
                # Konversi objek Mahasiswa ke dict
                data = [m.model_dump() for m in self.mahasiswa_list]
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error saving data: {e}")

    # CRUD: Create
    def tambah_mahasiswa(self, mhs: Mahasiswa):
        # Cek duplikasi NIM
        if any(m.nim == mhs.nim for m in self.mahasiswa_list):
            raise ValueError(f"Mahasiswa dengan NIM {mhs.nim} sudah ada.")
        
        self.mahasiswa_list.append(mhs)
        self.save_data()

    # CRUD: Read (All)
    def get_all_mahasiswa(self) -> List[Mahasiswa]:
        return self.mahasiswa_list

    # CRUD: Update
    def update_mahasiswa(self, nim: str, updated_data: Mahasiswa):
        for i, mhs in enumerate(self.mahasiswa_list):
            if mhs.nim == nim:
                # Update data, tapi jaga NIM tetap sama jika diperlukan, 
                # atau izinkan ganti jika validasi lolos (di sini kita replace object)
                self.mahasiswa_list[i] = updated_data
                self.save_data()
                return True
        return False

    # CRUD: Delete
    def hapus_mahasiswa(self, nim: str):
        original_len = len(self.mahasiswa_list)
        self.mahasiswa_list = [m for m in self.mahasiswa_list if m.nim != nim]
        
        if len(self.mahasiswa_list) < original_len:
            self.save_data()
            return True
        return False

    # Fitur: Sorting
    def sort_mahasiswa(self, algorithm: str, key: str, ascending: bool) -> List[Mahasiswa]:
        if algorithm == 'bubble':
            return SortingAlgorithms.bubble_sort(self.mahasiswa_list, key, ascending)
        elif algorithm == 'selection':
            return SortingAlgorithms.selection_sort(self.mahasiswa_list, key, ascending)
        elif algorithm == 'merge':
            return SortingAlgorithms.merge_sort(self.mahasiswa_list, key, ascending)
        else:
            return self.mahasiswa_list

    # Fitur: Searching
    def search_mahasiswa(self, method: str, query: str) -> List[Mahasiswa]:
        if method == 'binary':
            # Binary search spesifik untuk NIM
            result = SearchingAlgorithms.binary_search(self.mahasiswa_list, query)
            return [result] if result else []
        else:
            # Linear search bisa untuk Nama atau NIM (default implementation)
            # Kita cari di Nama dan NIM
            res_nama = SearchingAlgorithms.linear_search(self.mahasiswa_list, 'nama', query)
            res_nim = SearchingAlgorithms.linear_search(self.mahasiswa_list, 'nim', query)
            
            # Gabungkan hasil unik (set logic manual karena object equality)
            seen = set()
            combined = []
            for m in res_nama + res_nim:
                if m.nim not in seen:
                    combined.append(m)
                    seen.add(m.nim)
            return combined
