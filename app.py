import streamlit as st
import numpy_financial as npf
import pandas as pd

pages = [st.Page("pages/finCalcs.py", title="Financial Calculators"),
        st.Page("pages/loanCalcs.py", title="Loan Comparison")
    ]


pg = st.navigation(pages)
pg.run()
