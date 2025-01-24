import streamlit as st
from datetime import datetime
import requests
from nltk.corpus.reader import NOTES
from unicodedata import category

API_URL = "http://localhost:8000"

# Fix for outdated fetch_url module
try:
    from base64 import decodebytes, encodebytes  # Modern equivalents
    from Demos.security.sspi.fetch_url import options
except ImportError:
    # Fallback if fetch_url or its dependencies fail
    options = None  # Provide a default or mock implementation if required


def add_update_tab():
    date_selected = st.date_input(
        "Enter Date", datetime.now(), label_visibility="collapsed"
    )

    # Fetch existing expenses
    response = requests.get(f"{API_URL}/expenses/{date_selected}")
    if response.status_code == 200:
        existing_expenses = response.json()
        # st.write("Existing Expenses:", existing_expenses)
    else:
        st.error("Failed to retrieve expenses")
        existing_expenses = []

    # Categories
    categories = ["Rent", "Food", "Shopping", "Entertainment", "Other"]

    # Form for adding/updating expenses
    with st.form(key="expense_form"):
        expenses = []
        for i in range(5):
            if i < len(existing_expenses):
                amount = existing_expenses[i]['amount']
                category = existing_expenses[i]['category']
                notes = existing_expenses[i]['notes']
            else:
                amount = 0.0
                category = "Shopping"
                notes = ""

            col1, col2, col3 = st.columns(3)
            with col1:
                amount_input = st.number_input(
                    label=f"Amount {i + 1}",
                    min_value=0.0,
                    step=1.0,
                    value=amount,
                    key=f"amount_{i}",
                    label_visibility="collapsed"
                )
            with col2:
                category_input = st.selectbox(
                    label=f"Category {i + 1}",
                    options=categories,
                    index=categories.index(category),
                    key=f"category_{i}",
                    label_visibility="collapsed"
                )
            with col3:
                notes_input = st.text_input(
                    label=f"Notes {i + 1}",
                    value=notes,
                    key=f"notes_{i}",
                    label_visibility="collapsed"
                )

            expenses.append({
                'amount': amount_input,
                'category': category_input,
                'notes': notes_input
            })
        # Submit button
        submitted = st.form_submit_button("Submit")
        if submitted:
            filtered_expenses = [expense for expense in expenses if expense['amount'] > 0.0]

            response = requests.post(f"{API_URL}/expenses/{date_selected}", json=filtered_expenses)
            if response.status_code == 200:
                st.success("Expense Updated successfully")
            else:
                st.error("Failed to update expense")