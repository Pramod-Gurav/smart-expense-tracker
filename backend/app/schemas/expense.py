from pydantic import BaseModel
from datetime import date


class ExpenseCreate(BaseModel):
    amount: float
    description: str | None = None
    date: date


class ExpenseUpdate(BaseModel):
    amount: float
    description: str | None = None
    date: date


class ExpenseResponse(BaseModel):
    id: int
    amount: float
    description: str | None
    date: date

    class Config:
        from_attributes = True

