from sqlalchemy.orm import Session
from app.models.expense import Expense
from app.models.user import User
from datetime import date


def create_expense(
    db: Session,
    user: User,
    amount: float,
    description: str | None,
    expense_date: date
):
    expense = Expense(
        amount=amount,
        description=description,
        date=expense_date,
        user_id=user.id
    )
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


def get_user_expenses(db: Session, user: User):
    return db.query(Expense).filter(Expense.user_id == user.id).all()

from fastapi import HTTPException, status

def get_expense_by_id(db: Session, expense_id: int, user: User):
    expense = (
        db.query(Expense)
        .filter(Expense.id == expense_id, Expense.user_id == user.id)
        .first()
    )
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )
    return expense


def update_expense(
    db: Session,
    expense_id: int,
    user: User,
    amount: float,
    description: str | None,
    expense_date: date
):
    expense = get_expense_by_id(db, expense_id, user)
    expense.amount = amount
    expense.description = description
    expense.date = expense_date
    db.commit()
    db.refresh(expense)
    return expense


def delete_expense(db: Session, expense_id: int, user: User):
    expense = get_expense_by_id(db, expense_id, user)
    db.delete(expense)
    db.commit()

