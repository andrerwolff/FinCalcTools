import streamlit as st
import numpy_financial as npf
import pandas as pd
from datetime import date

st.title("Loan Amortization Calculator")

# Inputs
loan_amount = st.number_input("Loan Amount ($)", min_value=0.0, value=300000.0, icon=":material/attach_money:")
col1, col2 = st.columns(2)
with col1:   
    annual_rate = st.number_input("Annual Interest Rate (%)", min_value=0.0, value=4.5)
    origination_date = st.date_input("Origination Date", value=date(2023, 1, 1))

with col2:
    loan_term_years = st.number_input("Loan Term (Years)", min_value=1, value=30)
    first_payment_date = st.date_input("First Payment Date", value=date(2023, 2, 1))
st.markdown("---")

# Calculate
monthly_rate = annual_rate / 100 / 12
n_periods = loan_term_years * 12
monthly_payment = npf.pmt(monthly_rate, n_periods, -loan_amount)

# Generate amortization schedule
schedule = []
balance = loan_amount
for month in range(1, n_periods + 1):
    interest = balance * monthly_rate
    principal = monthly_payment - interest
    balance -= principal
    schedule.append({
        "Period": month,
        "Payment Date": (first_payment_date + pd.DateOffset(months=month-1)).strftime("%m/%d/%Y"),
        "Payment": monthly_payment,
        "Principal": principal,
        "Interest": interest,
        "Remaining Balance": balance
    })

# Convert to DataFrame
df = pd.DataFrame(schedule)

# Show first 12 rows, ellipsis, and last row
first_rows = df.head(12)
last_row = df.tail(1)
ellipsis_row = {
    "Period": "...",
    "Payment Date": "...",
    "Payment": "...",
    "Principal": "...",
    "Interest": "...",
    "Remaining Balance": "..."
}

# Combine the rows
condensed_df = pd.concat([first_rows, pd.DataFrame([ellipsis_row]), last_row], ignore_index=True)

# Pre-format the numeric columns (except the ellipsis row)
for col in ["Payment", "Principal", "Interest", "Remaining Balance"]:
    condensed_df[col] = condensed_df.apply(
        lambda row: f"${row[col]:,.2f}" if row["Period"] != "..." else "...",
        axis=1
    )



col3, col4 = st.columns(2)
with col3:
    st.write(f"### Monthly Payment: ${monthly_payment:,.2f}")
    st.write(f"### No. Payments Made: \n ### {df["Payment"].count()}")
with col4: 
    st.write(f"### Total Interest Paid: ${df['Interest'].sum():,.2f}")
    st.write(f"### Total Payments Made: ${df['Payment'].sum():,.2f}")

# Display the condensed table
with st.expander("Amortization Table", expanded=False):
    st.dataframe(condensed_df, hide_index=True)