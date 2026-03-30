import streamlit as st
import numpy_financial as npf
import pandas as pd

pages = {
    "Financial Calculators": [
        st.Page("pages/finCalcs.py", title="Financial Calculators"),
    ],
    "Others": [
        st.Page("pages/page2.py", title="Loan Comparison"),
    ]
}

pg = st.navigation(pages)
pg.run()
