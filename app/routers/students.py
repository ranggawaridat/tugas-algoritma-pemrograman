from fastapi import APIRouter, Depends, Request, Form, UploadFile, File, Response
from fastapi.responses import RedirectResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import require_user
from app.logic.student_manager import StudentManager
from app import models, schemas
from pydantic import ValidationError
import io

router = APIRouter(prefix="/students")
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
async def list_students(request: Request, user: models.User = Depends(require_user), db: Session = Depends(get_db)):
    mgr = StudentManager(db)
    students = mgr.get_all()
    return templates.TemplateResponse("students_list.html", {
        "request": request, 
        "user": user, 
        "students": students,
        "active_page": "students"
    })

@router.get("/add")
async def add_student_page(request: Request, user: models.User = Depends(require_user)):
    return templates.TemplateResponse("students_form.html", {
        "request": request,
        "user": user,
        "action": "Add",
        "active_page": "students"
    })

@router.post("/add")
async def add_student(
    request: Request,
    nama: str = Form(...),
    email: str = Form(...),
    nim: str = Form(...),
    jurusan: str = Form(...),
    ipk: float = Form(...),
    user: models.User = Depends(require_user),
    db: Session = Depends(get_db)
):
    mgr = StudentManager(db)
    try:
        # Validate using Pydantic
        student_in = schemas.StudentCreate(nama=nama, email=email, nim=nim, jurusan=jurusan, ipk=ipk)
        mgr.create(student_in)
        return RedirectResponse(url="/students", status_code=302)
    except Exception as e:
        return templates.TemplateResponse("students_form.html", {
            "request": request,
            "user": user,
            "action": "Add",
            "error": str(e),
            "form_data": {"nama": nama, "email": email, "nim": nim, "jurusan": jurusan, "ipk": ipk}
        })

@router.get("/edit/{student_id}")
async def edit_student_page(request: Request, student_id: int, user: models.User = Depends(require_user), db: Session = Depends(get_db)):
    mgr = StudentManager(db)
    student = mgr.get_by_id(student_id)
    if not student:
        return RedirectResponse(url="/students", status_code=302)
    
    return templates.TemplateResponse("students_form.html", {
        "request": request,
        "user": user,
        "action": "Edit",
        "student": student,
        "active_page": "students"
    })

@router.post("/edit/{student_id}")
async def edit_student(
    request: Request,
    student_id: int,
    nama: str = Form(...),
    email: str = Form(...),
    nim: str = Form(...),
    jurusan: str = Form(...),
    ipk: float = Form(...),
    user: models.User = Depends(require_user),
    db: Session = Depends(get_db)
):
    mgr = StudentManager(db)
    try:
        student_in = schemas.StudentUpdate(nama=nama, email=email, nim=nim, jurusan=jurusan, ipk=ipk)
        mgr.update(student_id, student_in)
        return RedirectResponse(url="/students", status_code=302)
    except Exception as e:
        # Need to reconstruct object to fill form
        mock_student = schemas.StudentResponse(id=student_id, nama=nama, email=email, nim=nim, jurusan=jurusan, ipk=ipk)
        return templates.TemplateResponse("students_form.html", {
            "request": request,
            "user": user,
            "action": "Edit",
            "error": str(e),
            "student": mock_student
        })

@router.get("/delete/{student_id}")
async def delete_student(student_id: int, user: models.User = Depends(require_user), db: Session = Depends(get_db)):
    mgr = StudentManager(db)
    mgr.delete(student_id)
    return RedirectResponse(url="/students", status_code=302)

@router.get("/export")
async def export_students(user: models.User = Depends(require_user), db: Session = Depends(get_db)):
    mgr = StudentManager(db)
    csv_content = mgr.export_csv()
    response = Response(content=csv_content, media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=students_export.csv"
    return response

@router.post("/import")
async def import_students(
    request: Request,
    file: UploadFile = File(...),
    user: models.User = Depends(require_user),
    db: Session = Depends(get_db)
):
    mgr = StudentManager(db)
    try:
        content = await file.read()
        text_content = content.decode("utf-8")
        count = mgr.import_csv(text_content)
        return RedirectResponse(url="/students", status_code=302)
    except Exception as e:
        students = mgr.get_all()
        return templates.TemplateResponse("students_list.html", {
            "request": request,
            "user": user,
            "students": students,
            "import_error": f"Import failed: {str(e)}"
        })
