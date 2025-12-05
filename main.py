from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from typing import List, Optional

from core.models import Mahasiswa
from core.manager import ManajemenMahasiswa

app = FastAPI(title="Manajemen Data Mahasiswa")

# Mount static files (CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates configuration
templates = Jinja2Templates(directory="templates")

# Initialize Manager
manager = ManajemenMahasiswa()

# --- Routes untuk GUI (Frontend) ---

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# --- API Endpoints (Backend) ---

@app.get("/api/mahasiswa", response_model=List[Mahasiswa])
async def get_mahasiswa(
    sort_by: Optional[str] = None, 
    order: Optional[str] = 'asc', 
    algo: Optional[str] = 'merge',
    search: Optional[str] = None,
    search_method: Optional[str] = 'linear'
):
    """
    Mengambil data mahasiswa dengan opsi sorting dan searching.
    """
    try:
        data = manager.get_all_mahasiswa()

        # Searching
        if search:
            data = manager.search_mahasiswa(search_method, search)

        # Sorting
        if sort_by:
            ascending = True if order == 'asc' else False
            # Kita sort hasil dari search (atau semua data)
            # Karena manager.sort_mahasiswa mengembalikan list baru dari self.mahasiswa_list,
            # kita perlu trik sedikit agar hanya mensort data yang sudah difilter search.
            # Tapi untuk simplifikasi tugas ini, kita panggil algoritma sorting langsung di sini
            # jika data sudah difilter search.
            
            if search:
                # Jika sudah ada hasil search, kita sort hasil itu saja
                # Menggunakan algoritma yang ada di manager tapi passing list manual agak tricky
                # karena method di manager pakai self.mahasiswa_list.
                # Kita akan gunakan method static di Algorithms langsung untuk fleksibilitas
                from core.algorithms import SortingAlgorithms
                
                if algo == 'bubble':
                    data = SortingAlgorithms.bubble_sort(data, sort_by, ascending)
                elif algo == 'selection':
                    data = SortingAlgorithms.selection_sort(data, sort_by, ascending)
                else:
                    data = SortingAlgorithms.merge_sort(data, sort_by, ascending)
            else:
                # Jika tidak ada search, pakai manager langsung
                data = manager.sort_mahasiswa(algo, sort_by, ascending)
                
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/mahasiswa", response_model=Mahasiswa)
async def create_mahasiswa(mahasiswa: Mahasiswa):
    try:
        manager.tambah_mahasiswa(mahasiswa)
        return mahasiswa
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/mahasiswa/{nim}", response_model=Mahasiswa)
async def update_mahasiswa(nim: str, mahasiswa: Mahasiswa):
    try:
        if nim != mahasiswa.nim:
             raise HTTPException(status_code=400, detail="NIM di URL dan body tidak cocok")
             
        success = manager.update_mahasiswa(nim, mahasiswa)
        if not success:
            raise HTTPException(status_code=404, detail="Mahasiswa tidak ditemukan")
        return mahasiswa
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/mahasiswa/{nim}")
async def delete_mahasiswa(nim: str):
    success = manager.hapus_mahasiswa(nim)
    if not success:
        raise HTTPException(status_code=404, detail="Mahasiswa tidak ditemukan")
    return {"message": "Data berhasil dihapus"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
