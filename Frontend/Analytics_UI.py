import streamlit as st
from datetime import datetime
import requests
import pandas as pd
from nltk.corpus.reader import NOTES
from unicodedata import category

API_URL = "http://localhost:8000"

try:
    from base64 import decodebytes, encodebytes  # Modern equivalents
    from Demos.security.sspi.fetch_url import options
except ImportError:
    # Fallback if fetch_url or its dependencies fail
    options = None  # Provide a default or mock implementation if required

def analytics_tab():
    col1,col2=st.columns(2)
    with col1:
        start_date=st.date_input("Start Date",datetime(2024,8,1))
    with col2:
        end_date=st.date_input("End Date",datetime(2024,8,5))

    if st.button("Get Analytics"):
        payload={
            "start_date":start_date.strftime("%Y-%m-%d"),
            "end_date":end_date.strftime("%Y-%m-%d")
        }

        response=requests.post(f"{API_URL}/Analytics/",json=payload)

        response=response.json()

        data={
            "category":list(response.keys()),
            "Total":[response[category]["total"] for category in response],
            "Percentage":[response[category]["percentage"] for category in response]

        }
        # st.write(response)
        df=pd.DataFrame(data)
        df_sorted=df.sort_values(by="Percentage",ascending=False)

        st.title("Expense Breakdown by category")
        st.bar_chart(data=df_sorted.set_index("category")['Percentage'],width=0,height=0)
        df_sorted["Total"]=df_sorted["Total"].map("{:.2f}".format)

        df_sorted["Percentage"] = df_sorted["Percentage"].map("{:.2f}".format)

        st.table(df_sorted)