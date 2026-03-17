from backend import db_helper

# Test for fetch expenses for date
def test_fetch_expenses_for_date_valid():
    expenses =  db_helper.fetch_expenses_for_date('2024-08-15')

    assert len(expenses) == 1
    assert expenses[0]['amount'] == 10.0

# Test for fetch expenses for invalid date
def test_fetch_expenses_for_date_invalid():
    expenses =  db_helper.fetch_expenses_for_date('9999-08-15')

    assert len(expenses) == 0

# Test for fetch expenses summery for invalid date range
def test_fetch_expenses_summery_invalid():
    summery =  db_helper.fetch_expenses_summery('2030-08-02','2030-08-03')

    assert len(summery) == 0






