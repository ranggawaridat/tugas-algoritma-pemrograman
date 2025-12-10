from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import require_user
from app.logic.student_manager import StudentManager
from app import models

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
async def landing(request: Request):
    return templates.TemplateResponse("landing.html", {"request": request})

@router.get("/dashboard")
async def dashboard(request: Request, user: models.User = Depends(require_user), db: Session = Depends(get_db)):
    mgr = StudentManager(db)
    students = mgr.get_all()
    
    total_students = len(students)
    avg_ipk = sum([s.ipk for s in students]) / total_students if total_students > 0 else 0
    jurusan_counts = {}
    for s in students:
        jurusan_counts[s.jurusan] = jurusan_counts.get(s.jurusan, 0) + 1
        
    stats = {
        "total_students": total_students,
        "avg_ipk": round(avg_ipk, 2),
        "jurusan_counts": jurusan_counts
    }
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request, 
        "user": user, 
        "stats": stats,
        "active_page": "dashboard"
    })
