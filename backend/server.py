from fastapi import FastAPI, HTTPException
import uvicorn
from datetime import date
import db_helper
from typing import List
from pydantic import BaseModel

app = FastAPI()

# For data validation/dtype
class Expense(BaseModel):
    amount: float
    category: str
    notes: str

class DateRange(BaseModel):
    start_date: date
    end_date: date

# Get expenses for date
# response model is used to pull required/valid data
# List for store in list
@app.get("/expenses/{expense_date}", response_model= List[Expense])
def get_expenses(expense_date: date):
    expenses = db_helper.fetch_expenses_for_date(expense_date)
    if expenses is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve expense from the database")

    return expenses

# For Add/Update expenses
@app.post("/expenses/{expense_date}")
def add_or_update_expense(expense_date: date, expenses:List[Expense]): # here validate the data
    # first delete the records then go for insert
    db_helper.delete_expenses_for_date(expense_date)
    # For loop: may be many inserted records
    for expense in expenses: 
        db_helper.insert_expense(expense_date, expense.amount, expense.category, expense.notes)
    return {"message": "Expenses updated successfully"}


@app.post("/analytics/")
def get_analytics(date_range: DateRange):
    # call summery func
    data = db_helper.fetch_expenses_summery(date_range.start_date, date_range.end_date)
    if data is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve expense summery from the database")


    total = sum([row['total'] for row in data])

    breackdown = {}
    for row in data:
        percentage = (row['total'] / total) * 100 if total != 0 else 0

        # To store total & pct by each category
        breackdown[row['category']] = {
                    "total": row['total'],
                    "percentage": percentage
                }

    return breackdown


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)