import mysql.connector
from contextlib import contextmanager
from logging_setup import setup_logger

# provides logger & file name or level (default= logging.DEBUG)
logger = setup_logger('db_helper', 'server.log')

@contextmanager  # used will able to return func by yeild
def get_db_cursor(commit=False):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="expense_manager"
    )
    # # To test db connect or not
    # if connection.is_connected():
    #     print("Connection successful")
    # else:
    #     print("Failed in connection to database")

    cursor = connection.cursor(dictionary=True)
    yield cursor
    # We will be commit where have update & delete
    if commit: # This will be run when commit is True
        connection.commit()
    print("Closing cursor")
    cursor.close()
    connection.close()

def fetch_expenses_for_date(expense_date):
    logger.info(f"fetch_expenses_for_date for {expense_date}")
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses WHERE expense_date = %s", (expense_date,))
        expenses = cursor.fetchall()
        # for expense in expenses:
        #     print(expense)
        return expenses

def insert_expense(expense_date, amount, category, notes):
    logger.info(f"insert_expense with date: {expense_date}, amount: {amount}, category: {category}, notes: {notes}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)",
            (expense_date, amount, category, notes)
        )
        # print("Expenses updated successfully")
def delete_expenses_for_date(expense_date):
    logger.info(f"delete_expenses_for_date for {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date = %s", (expense_date,)
        )
        # print("Expenses deleted successfully")

def fetch_expenses_summery(start_date, end_date):
    logger.info(f"fetch_expenses_summery with start: {start_date} end: {end_date}")
    with get_db_cursor() as cursor:
        cursor.execute('''SELECT category, sum(amount) as total FROM expenses 
        where expense_date between %s and %s
        group by category;
        ''',(start_date, end_date)
        )
        data = cursor.fetchall()
        return data


if __name__ == "__main__":
    sum = fetch_expenses_summery('2024-08-02','2024-08-03')
    for i in sum:
         print(i)
    # expenses = fetch_expenses_for_date("2024-08-15")
    # print(expenses)
    # insert_expense("2024-08-21", 300, "Food", "Panipuri")
    # delete_expenses_for_date("2024-08-20")