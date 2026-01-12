from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.expense import ExpenseCreate, ExpenseResponse
from app.core.dependencies import get_current_user, get_db
from app.services.expense_service import create_expense, get_user_expenses
from app.models.user import User

from app.schemas.expense import ExpenseUpdate
from app.services.expense_service import update_expense, delete_expense


router = APIRouter(prefix="/expenses", tags=["Expenses"])


@router.post("/", response_model=ExpenseResponse)
def add_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_expense(
        db=db,
        user=current_user,
        amount=expense.amount,
        description=expense.description,
        expense_date=expense.date
    )


@router.get("/", response_model=list[ExpenseResponse])
def list_expenses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_user_expenses(db, current_user)
    
    
@router.put("/{expense_id}", response_model=ExpenseResponse)
def edit_expense(
    expense_id: int,
    expense: ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_expense(
        db=db,
        expense_id=expense_id,
        user=current_user,
        amount=expense.amount,
        description=expense.description,
        expense_date=expense.date
    )


@router.delete("/{expense_id}", status_code=204)
def remove_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    delete_expense(db, expense_id, current_user)


