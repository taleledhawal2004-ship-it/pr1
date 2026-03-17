import streamlit as st
from datetime import datetime
import requests
import  time

# endpoint from backend
# 127.0.0.2 this means localhost
API_URL = "http://127.0.0.1:8000"

def add_update_tab():
    selected_date = st.date_input("Enter Date", datetime.now().date(), label_visibility="collapsed")
    # get response for selected date
    response = requests.get(f"{API_URL}/expenses/{selected_date}")
    # check status code 
    if response.status_code == 200:
        existing_expenses = response.json()
    else:
        st.error("Failed to retrieve expenses")
        existing_expenses = []

    # st.write(len(existing_expenses))


    categories = ["Rent", "Food", "Shopping", "Entertainment", "Other"]

    # Form for show cols
    with st.form(key="expense_form"):
        # create 3 col to write main col name
        col1, col2, col3 = st.columns(3)
        with col1:
            st.text("Amount")
        with col2:
            st.text("Category")
        with col3:
            st.text("Notes")

        expenses = []
        # loop for rows
        for i in range(5):
            # check data for selected date
            if i < len(existing_expenses):
                amount = existing_expenses[i]['amount']
                category = existing_expenses[i]['category']
                notes = existing_expenses[i]['notes']
            else:
                amount = 0.0
                category = "Food"
                notes = ""

            # create 3 col to show data
            col1, col2, col3 = st.columns(3)
            with col1:
                amount_inp = st.number_input(label="Amount", min_value=0.0, step=10.0, value=amount, key=f"amount_{i}",
                                             label_visibility="collapsed")
            with col2:
                category_inp = st.selectbox(label="Category", options=categories, index=categories.index(category),
                                            key=f"category_{i}", label_visibility="collapsed")
            with col3:
                notes_inp = st.text_input(label="Notes", key=f"notes_{i}", value=notes, label_visibility="collapsed")

            # store input into list as dict
            expenses.append({
                'amount': amount_inp,
                'category': category_inp,
                'notes': notes_inp
            }) 


        # submit button
        submit_button = st.form_submit_button(label="Submit")
        if submit_button:
            # filter for amount > 0
            filtered_expenses = [expense for expense in expenses if expense['amount'] > 0]
            # Add/Update data by Post
            response = requests.post(f"{API_URL}/expenses/{selected_date}", json=filtered_expenses)
            if response.status_code == 200:
                success_msg = st.success("Expenses updated successfully")
                time.sleep(4)  # Display message for 3 seconds
                success_msg.empty()  # Clear the message after the wait
            else:
                error_msg = st.error("Failed to retrieve expenses")
                time.sleep(4)  # Display message for 3 seconds
                error_msg.empty()  # Clear the message after the wait
