from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.services.analytics_service import monthly_summary

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/monthly")
def get_monthly_analytics(
    year: int,
    month: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return monthly_summary(db, current_user, year, month)

