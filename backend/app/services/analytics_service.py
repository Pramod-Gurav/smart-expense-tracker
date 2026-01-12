from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date

from app.models.expense import Expense
from app.models.category import Category
from app.models.user import User


def monthly_summary(db: Session, user: User, year: int, month: int):
    start_date = date(year, month, 1)

    if month == 12:
        end_date = date(year + 1, 1, 1)
    else:
        end_date = date(year, month + 1, 1)

    total = (
        db.query(func.sum(Expense.amount))
        .filter(
            Expense.user_id == user.id,
            Expense.date >= start_date,
            Expense.date < end_date
        )
        .scalar()
    ) or 0

    category_breakdown = (
        db.query(Category.name, func.sum(Expense.amount))
        .join(Expense)
        .filter(
            Expense.user_id == user.id,
            Expense.date >= start_date,
            Expense.date < end_date
        )
        .group_by(Category.name)
        .all()
    )

    return {
        "total": total,
        "categories": [
            {"category": name, "amount": amount}
            for name, amount in category_breakdown
        ]
    }

