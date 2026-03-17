import streamlit as st
from datetime import datetime
import requests
import pandas as pd

# endpoint from backend
# 127.0.0.2 this means localhost
API_URL = "http://127.0.0.1:8000"

def analytics_tab():
    # For give date range as input
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime(2024, 8, 15))
        # st.write(start_date)
    with col2:
        end_date = st.date_input("End Date", datetime(2024, 8, 17))


    if st.button("Get Analytics"):
        payload = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d")
        }
        # get response for selected date
        response = requests.post(f"{API_URL}/analytics/", json=payload)
        data = response.json()
        # st.write(data)

        data = {
            "Category": list(data.keys()),
            "Total": [data[category]['total'] for category in data],
            "Percentage": [data[category]['percentage'] for category in data]
        }
        # create df
        df = pd.DataFrame(data)
        df_sorted = df.sort_values(by="Percentage", ascending=False) 

        # Plot chart
        st.title("Expense By Category")
        st.bar_chart(data=df_sorted.set_index('Category')['Percentage'], width=0, height=0,
                     use_container_width=True)

        df_sorted["Total"] = df_sorted["Total"].map("{:.2f}".format)
        df_sorted["Percentage"] = df_sorted["Percentage"].map("{:.2f}".format)

        st.table(df_sorted)


        # # check status code
        # if response.status_code == 200:
        #     existing_expenses = response.json()
        # else:
        #     st.error("Failed to retrieve expenses")
        #     existing_expenses = []

