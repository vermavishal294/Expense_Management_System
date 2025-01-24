from operator import index

import streamlit as st
from datetime import datetime
import requests
from nltk.corpus.reader import NOTES
from unicodedata import category
from Add_update import add_update_tab
from Analytics_UI import analytics_tab
from Add_update import add_update_tab
from Analytics_UI import analytics_tab
from Analytics_By_month import analytics_months_tab

API_URL = "http://localhost:8000"

st.title("Expense Management System")
tab1,tab2,tab3= st.tabs(["Add/Update","Analytics by category","Analytics by month"])

with tab1:
    add_update_tab()
with tab2:
    analytics_tab()
with tab3:
    analytics_months_tab()
