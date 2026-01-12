from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.category import CategoryCreate, CategoryResponse
from app.services.category_service import create_category, get_categories
from app.core.dependencies import get_db, get_current_user
from app.models.user import User

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/", response_model=CategoryResponse)
def add_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_category(db, current_user, category.name)


@router.get("/", response_model=list[CategoryResponse])
def list_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_categories(db, current_user)

