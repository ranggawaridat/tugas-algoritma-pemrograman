from fastapi import Request, Depends, HTTPException, status
from jose import jwt, JWTError
from app.core.config import settings
from app.database import get_db
from sqlalchemy.orm import Session
from app import models

async def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        return None
    
    try:
        scheme, token_str = token.split()
        if scheme.lower() != 'bearer':
            return None
        payload = jwt.decode(token_str, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
    except (JWTError, ValueError):
        return None
        
    user = db.query(models.User).filter(models.User.email == email).first()
    return user

async def require_user(request: Request, user: models.User = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=status.HTTP_302_FOUND, headers={"Location": "/login"})
    return user
