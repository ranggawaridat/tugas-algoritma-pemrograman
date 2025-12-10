from fastapi import APIRouter, Depends, HTTPException, status, Request, Response, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.core import security
from app.core.config import settings

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.email == username).first() # Using email as username
    if not user or not security.verify_password(password, user.hashed_password):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Kredensial tidak valid"})
    
    access_token = security.create_access_token(data={"sub": user.email})
    response = RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return response

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register")
async def register(
    request: Request,
    nama: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        if len(password) > 72:
             return templates.TemplateResponse("register.html", {"request": request, "error": "Kata sandi tidak boleh lebih dari 72 karakter"})

        user_exists = db.query(models.User).filter(models.User.email == email).first()
        if user_exists:
            return templates.TemplateResponse("register.html", {"request": request, "error": "Email sudah terdaftar"})
        
        hashed_pw = security.get_password_hash(password)
        new_user = models.User(email=email, hashed_password=hashed_pw, nama=nama)
        db.add(new_user)
        db.commit()
        
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    except Exception as e:
        db.rollback()
        import traceback
        return templates.TemplateResponse("register.html", {"request": request, "error": f"Pendaftaran gagal: {str(e)}"})

@router.get("/logout")
async def logout(response: Response):
    response = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("access_token")
    return response
