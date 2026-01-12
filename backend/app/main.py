from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.routers import auth, expenses
from app.routers import analytics

app.include_router(analytics.router)

app = FastAPI(title="Smart Expense Tracker API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(expenses.router)


@app.get("/")
def root():
    return {"message": "Smart Expense Tracker backend is running "}

from app.db.database import engine
from app.models.expense import Expense

Expense.metadata.create_all(bind=engine)

from app.routers import auth, expenses, categories

app.include_router(auth.router)
app.include_router(expenses.router)
app.include_router(categories.router)

from app.db.database import engine
from app.models.category import Category

Category.metadata.create_all(bind=engine)

