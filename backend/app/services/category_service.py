from sqlalchemy.orm import Session
from app.models.category import Category
from app.models.user import User
from fastapi import HTTPException, status


def create_category(db: Session, user: User, name: str):
    existing = (
        db.query(Category)
        .filter(Category.user_id == user.id, Category.name == name)
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category already exists"
        )

    category = Category(name=name, user_id=user.id)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def get_categories(db: Session, user: User):
    return db.query(Category).filter(Category.user_id == user.id).all()

