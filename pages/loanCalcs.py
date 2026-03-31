import streamlit as st
import numpy as np
import numpy_financial as npf
import pandas as pd
import plotly.express as px
from datetime import date

st.title("Loan Amortization Calculator")
if "adv_recur_extra_payments" not in st.session_state:
    st.session_state.adv_recur_extra_payments = []
if "lump_sum_payments" not in st.session_state:
    st.session_state.lump_sum_payments = []

with st.sidebar:
    expr = st.text_input("Quick Math:")
    if expr:
        try:
            result = eval(expr)
            st.code(f"{result}", language="python",width="content")
        except:
            st.error("Invalid expression")



def calculate_extra_payment(period):
    extra_payment = 0.0
    # Regular recurring extra payment
    if st.session_state.get("recurring_extra_payment", 0) > 0:
        frequency = st.session_state.get("recurring_extra_payment_frequency", "Monthly")
        freq_map = {"Monthly": 1, "Quarterly": 3, "Semi-Annually": 6, "Yearly": 12}
        if (period - 1) % freq_map[frequency] == 0:
            extra_payment += st.session_state["recurring_extra_payment"]
    
    # Advanced recurring extra payments
    for payment in st.session_state.adv_recur_extra_payments:
        if payment["start"] <= period <= payment["end"] and (period - payment["start"]) % payment["frequency"] == 0:
            extra_payment += payment["amount"]
    
    # Lump sum payments
    for payment in st.session_state.lump_sum_payments:
        if payment["period"] == period:
            extra_payment += payment["amount"]
    
    return extra_payment


# Basic Inputs
col1, col2 = st.columns(2)
with col1:   
    loan_amount = st.number_input("Loan Amount", min_value=0.0, value=522800.0, icon=":material/attach_money:")
    loan_term_years = st.number_input("Loan Term (Years)", min_value=1, value=30)
with col2:
    annual_rate = st.number_input("Annual Interest Rate (%)", min_value=0.0, value=6.125)
    first_payment_date = st.date_input("First Payment Date", value=date(2026, 2, 1), format="MM/DD/YYYY")

#Advanced Inputs
with st.expander("Advanced Options", expanded=False):
    # Additional Payments
    if st.checkbox("Add Additional Payments", value=False, key="add_additional_payments"):
        # Recurring Extra Monthly Payments
        with st.expander("Recurring Extra Payments", expanded=False):
            col_l1_1,col_l1_2 = st.columns(2)
            with col_l1_1:
                recur_extra_payment = st.number_input(
                    "Recurring Extra Payment (for the life of the loan)",
                    min_value=0.0,
                    value=0.0,
                    key="recurring_extra_payment",
                    icon=":material/attach_money:"
            )
            with col_l1_2:
                recur_extra_payment_frequency = st.selectbox(
                    "Frequency of Recurring Extra Payments",
                    options=["Monthly", "Quarterly", "Semi-Annually", "Yearly"],
                    key="recurring_extra_payment_frequency"
                )
            # Advanced Recurring Payments with Custom Frequency and Duration
            if st.checkbox("Advanced Recurring Payments"):
                if st.button("Add Advanced Recurring Payment"):
                    st.session_state.adv_recur_extra_payments.append({
                        "amount": 0.0,
                        "frequency": 1,
                        "start": 1,
                        "end": loan_term_years * 12
                    })
                    st.rerun()

                for i, payment in enumerate(st.session_state.adv_recur_extra_payments):
                    col_a1, col_a2, col_a3, col_a4, col_a5 = st.columns(5)
                    with col_a1:
                        payment["amount"] = st.number_input(
                            f"Amount {i+1}",
                            min_value=0.0,
                            value=payment["amount"],
                            key=f"adv_recurring_extra_payment_{i}",
                            icon=":material/attach_money:"
                        )
                    with col_a2:
                        payment["frequency"] = st.number_input(
                            f"Freq. (every x pds)",
                            min_value=1,
                            value=payment["frequency"],
                            key=f"adv_recurring_extra_payment_frequency_{i}"
                        )
                    with col_a3:
                        payment["start"] = st.number_input(
                            f"Start Period",
                            min_value=1,
                            value=payment["start"],
                            key=f"adv_recur_extra_payment_start_{i}"
                        )
                    with col_a4:
                        payment["end"] = st.number_input(
                            f"End Period",
                            min_value=1,
                            value=payment["end"],
                            key=f"adv_recur_extra_payment_end_{i}"
                        )
                    with col_a5:
                        if st.button(f"Remove", key=f"remove_adv_recur_{i}"):
                            st.session_state.adv_recur_extra_payments.pop(i)
                            st.rerun()

        # Lump Sum Payments at Given Periods
        with st.expander("Lump Sum Payments at Given Periods", expanded=False):
            if st.button("Add Lump Sum Payment"):
                st.session_state.lump_sum_payments = st.session_state.get("lump_sum_payments", []) + [{"period": 1, "amount": 0.0}]
            if "lump_sum_payments" in st.session_state:
                for i, payment in enumerate(st.session_state.lump_sum_payments):
                    col1, col2, col3 = st.columns(3)
                    with col2:
                        payment["period"] = st.number_input(
                            f"Period",
                            min_value=1,
                            value=payment["period"],
                            key=f"lump_sum_period_{i}"
                        )
                    with col1:
                        payment["amount"] = st.number_input(
                            f"Amount {i+1}",
                            min_value=0.0,
                            value=payment["amount"],
                            key=f"lump_sum_amount_{i}",
                            icon=":material/attach_money:"
                        )
                    with col3:
                        if st.button(f"Remove", key=f"remove_lump_sum_{i}"):
                            st.session_state.lump_sum_payments.pop(i)
                            st.rerun()

    st.checkbox("Tax Deductible Interest", value=False, key="tax_deductible")
    origination_date = st.date_input("Origination Date", value=date(2026, 1, 1), format="MM/DD/YYYY")


#with st.expander("Debug: Current Extra Payments State", expanded=False):
#    try:
#        st.write("Regular Extra Payment:", recur_extra_payment, "every", recur_extra_payment_frequency)
#        st.write("Advanced Recurring Payments:", st.session_state.adv_recur_extra_payments)
#       st.write("Lump Sum Payments:", st.session_state.lump_sum_payments)
#        st.write("extra payment for period 1:", calculate_extra_payment(1))
#    except Exception as e:
#        st.write("No additional payments defined yet.")
st.markdown("---")

# Calculate
monthly_rate = annual_rate / 100 / 12
n_periods = loan_term_years * 12
monthly_payment = npf.pmt(monthly_rate, n_periods, -loan_amount)

# Generate amortization schedule
schedule = []
balance = loan_amount
payoff_month = n_periods
for month in range(1, n_periods + 1):

    extra_payment = calculate_extra_payment(month)
    interest = balance * monthly_rate
    principal = monthly_payment - interest

    # Check if the loan is paid off this month
    if balance > 0:
        if balance + interest <= monthly_payment + extra_payment:
            principal = balance
            monthly_payment = principal + interest - extra_payment
            balance = 0
            payoff_month = month
        else:
            balance -= principal + extra_payment
    else:
        monthly_payment = 0
        interest = 0
        principal = 0
        extra_payment = 0

    schedule.append({
        "Period": month,
        "Payment Date": (first_payment_date + pd.DateOffset(months=month-1)).strftime("%m/%d/%Y"),
        "Payment": monthly_payment,
        "Principal": principal,
        "Interest": interest,
        "Extra Payment": extra_payment,
        "Remaining Balance": balance
    })

# Convert to DataFrame
df = pd.DataFrame(schedule)

# Toggle for condensed view
with st.expander("Amortization Table", expanded=False):
    condensed_view = st.checkbox("Condense Table", value=False, key="condensed_view")

    if condensed_view:
        # Range slider to select which rows to omit
        min_row, max_row = st.slider(
            "Select Rows to Omit",
            min_value=1,
            max_value=len(df),
            value=(13, len(df) - 12),  # Default: omit middle rows, show first 12 and last 12
            key="omit_rows"
        )

        # Split the DataFrame into parts to keep
        first_rows = df.iloc[:min_row]
        last_rows = df.iloc[max_row:]

        # Create ellipsis row with NaN for all numeric columns
        ellipsis_row = pd.DataFrame({
            "Period": [np.nan],
            "Payment Date": ["..."],
            "Payment": [np.nan],
            "Principal": [np.nan],
            "Interest": [np.nan],
            "Remaining Balance": [np.nan],
            "Extra Payment": [np.nan]
        })

        # Combine rows
        condensed_df = pd.concat([first_rows, ellipsis_row, last_rows], ignore_index=True)

        st.dataframe(
            condensed_df.style.format({
                "Period": "{:.0f}",
                "Payment": "${:,.2f}",
                "Principal": "${:,.2f}",
                "Interest": "${:,.2f}",
                "Remaining Balance": "${:,.2f}",
                "Extra Payment": "${:,.2f}"
            }, na_rep=""),  # Display NaN as empty string
            hide_index=True
        )

    else:
        # Display full table
        st.dataframe(df.style.format({
            "Payment": "${:,.2f}",
            "Principal": "${:,.2f}",
            "Interest": "${:,.2f}",
            "Remaining Balance": "${:,.2f}",
            "Extra Payment": "${:,.2f}"
        }), hide_index=True)


#---- Analysis ----
# Calculate total interest paid, assuming no additional payments
monthly_payment_analysis = npf.pmt(monthly_rate, n_periods, -loan_amount)
total_interest_no_extra = monthly_payment_analysis * n_periods - loan_amount
total_interest_with_extra = df["Interest"].sum()
interest_saved = total_interest_no_extra - total_interest_with_extra
extra_payments = df["Extra Payment"].values
cash_flows = list(-extra_payments)
cash_flows.append(interest_saved)  # Add interest saved as a positive cash flow at the end
irr = npf.irr(cash_flows)  # Monthly IRR
annualized_irr = (1 + irr) ** 12 - 1 # Annualize the IRR


# Count the number of payments made (non-zero payments)
num_payments_made = len([p for p in schedule if p["Payment"] > 0])

# Find the payoff date (when balance first reaches zero)
payoff_date = (first_payment_date + pd.DateOffset(months=payoff_month-1)).strftime("%m/%d/%Y")

col3, col4 = st.columns(2)
with col3:
    st.write(f"### Monthly Payment: ${monthly_payment_analysis:,.2f}")
    st.write(f"### Payoff Date: {payoff_date}")
    st.write(f"### NO. Payments Made:    {num_payments_made}")
with col4: 
    st.write(f"### Total Interest Paid: ${total_interest_with_extra:,.2f}")
    st.write(f"### Total Payments Made: ${df['Payment'].sum():,.2f}")
    if st.session_state.get("add_additional_payments", False):
        st.write(f"### Total Extra Paid:    ${df['Extra Payment'].sum():,.2f}")
        st.write (f"### IRR of Extra Payments:  {annualized_irr*100:.2f}%")

