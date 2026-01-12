from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.schemas.user import UserCreate, UserLogin
from app.services.auth_service import create_user, authenticate_user
from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    new_user = create_user(db, user.email, user.password)
    return {"id": new_user.id, "email": new_user.email}


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    authenticated_user = authenticate_user(db, user.email, user.password)
    if not authenticated_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": authenticated_user.email})
    return {"access_token": token, "token_type": "bearer"}

