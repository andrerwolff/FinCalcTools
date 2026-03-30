from altair import value
import streamlit as st
import numpy_financial as npf

st.title("Financial Calculators")

# Sidebar for navigation
with st.sidebar:
    calculator = st.radio(
        "Select a Calculator:",
        ["Future Value (FV)", "Present Value (PV)", "Payment (PMT)", "Interest Rate (i)", "Time Period (n)"]
    )

st.title(f"{calculator} Calculator")

def compute_factors(time_unit, comp_freq):
    """
    Compute the time factor and interest rate factor based on time unit and compounding frequency.

    Args:
        time_unit (str): The unit of time (e.g., "Years", "Months", "Quarters", "Weeks", "Days").
        comp_freq (str): The compounding frequency (e.g., "Annually", "Monthly", "Quarterly", "Weekly", "Daily").

    Returns:
        float: The time factor to convert time to periods, and rate to appropriate periodic rate.
    """
    # Determine time factor
    if time_unit == "Years":
        if comp_freq == "Annually":
            factor = 1
        elif comp_freq == "Quarterly":
            factor = 4
        elif comp_freq == "Monthly":
            factor = 12
        elif comp_freq == "Weekly":
            factor = 52
        elif comp_freq == "Daily":
            factor = 365
    elif time_unit == "Quarters":
        if comp_freq == "Annually":
            factor = 0.25
        elif comp_freq == "Quarterly":
            factor = 1
        elif comp_freq == "Monthly":
            factor = 3
        elif comp_freq == "Weekly":
            factor = 13
        elif comp_freq == "Daily":
            factor = 91.25
    elif time_unit == "Months":
        if comp_freq == "Annually":
            factor = 1/12
        elif comp_freq == "Quarterly":
            factor = 1/3
        elif comp_freq == "Monthly":
            factor = 1
        elif comp_freq == "Weekly":
            factor = 4.33
        elif comp_freq == "Daily":
            factor = 30.44
    elif time_unit == "Weeks":
        if comp_freq == "Annually":
            factor = 1/52
        elif comp_freq == "Quarterly":
            factor = 1/13
        elif comp_freq == "Monthly":
            factor = 1/4.33
        elif comp_freq == "Weekly":
            factor = 1
        elif comp_freq == "Daily":
            factor = 7
    elif time_unit == "Days":
        if comp_freq == "Annually":
            factor = 1/365
        elif comp_freq == "Quarterly":
            factor = 1/91.25
        elif comp_freq == "Monthly":
            factor = 1/30.44
        elif comp_freq == "Weekly":
            factor = 1/7
        elif comp_freq == "Daily":
            factor = 1

    return factor


# Initialize session state for scenarios
if 'scenarios' not in st.session_state:
    st.session_state.scenarios = {
        "FV": [],
        "PV": [],
        "PMT": [],
        "I": [],
        "n": []
    }

# Function to save current scenario
def save_scenario(calculator_type, inputs, result):
    scenario_name = f"Scenario {len(st.session_state.scenarios[calculator_type]) + 1}"
    st.session_state.scenarios[calculator_type].append({
        "name": scenario_name,
        "inputs": inputs,
        "result": result
    })

# Function to display scenarios for the current calculator type
def display_scenarios(calculator_type):
    scenarios = st.session_state.scenarios[calculator_type]
    if not scenarios:
        st.write("No scenarios saved yet.")
        return

    st.header("Comparison")
    cols = st.columns(len(scenarios))
    for i, scenario in enumerate(scenarios):
        with cols[i]:
            st.subheader(scenario["name"])
            st.write(f"**Result:** {scenario['result']}")
            with st.expander("**Inputs**", expanded=True):
                for key, value in scenario["inputs"].items():
                    st.write(f"- {key}: {value}")
            if st.button(f"Remove", key=f"remove_{calculator_type}_{i}"):
                st.session_state.scenarios[calculator_type].pop(i)
                st.rerun()


time_unit = "Years"  # Default time unit
comp_freq = "Annually"  # Default compounding frequency

if calculator == "Future Value (FV)":
    st.markdown("""Calculate the **Future Value** of an investment or loan based on a series of regular payments and a fixed interest rate.""")
    col1, col2 = st.columns(2)
    with col1:
        pv = st.number_input("Present Value (PV)", value=1000.0, step=50.0, icon=":material/attach_money:")
        cola, colb = st.columns(2)
        with cola:
            time = st.number_input("Time", min_value=0, value=10)
        with colb:
            time_unit = st.selectbox("Time Unit", ["Years", "Quarters", "Months", "Weeks", "Days"])
        

    with col2:
        pmt = st.number_input("Payment (PMT)", value=0.0, step=50.0, icon=":material/attach_money:")
        cola, colb = st.columns(2)
        with cola:
            comp_freq = st.selectbox("Compounding Frequency", ["Annually", "Quarterly", "Monthly", "Weekly", "Daily"])
        with colb:
            n = st.number_input("Number of Periods (n)", value=time * compute_factors(time_unit, comp_freq),disabled=True)
    
    colc, cold = st.columns(2)
    with colc:
        rate = st.number_input("Interest Rate/Time Unit (%)", min_value=0.0, value=5.0, step=.125)
    with cold:
        p_rate = st.number_input("Periodic Interest Rate (i) (%)", value=rate / compute_factors(time_unit, comp_freq), disabled=True)  # Convert to periodic rate based on time unit
    
    fv = npf.fv(p_rate/100, n, pmt, -pv)
    st.write(f"## Future Value: ${fv:,.2f}")

    # Save Scenario button
    if st.button("Save Scenario"):
        save_scenario("FV", {"pv": pv, "pmt": pmt, "rate": rate, "n": n, "time": time, "time_unit": time_unit, "comp_freq": comp_freq}, f"${fv:,.2f}")
        st.rerun()

    # Display FV scenarios
    display_scenarios("FV")


elif calculator == "Present Value (PV)":
    st.markdown("""Calculate the **Present Value** of a future sum of money or series of payments, discounted at a specific interest rate.""")
    col1, col2 = st.columns(2)
    with col1:
        fv = st.number_input("Future Value (FV)", value=1000.0, step=50.0, icon=":material/attach_money:")
        cola, colb = st.columns(2)
        with cola:
            time = st.number_input("Time", min_value=0, value=10)
        with colb:
            time_unit = st.selectbox("Time Unit", ["Years", "Quarters", "Months", "Weeks", "Days"])

    with col2:
        pmt = st.number_input("Payment (PMT)", value=0.0, step=50.0, icon=":material/attach_money:")
        cola, colb = st.columns(2)
        with cola:
            comp_freq = st.selectbox("Compounding Frequency", ["Annually", "Quarterly", "Monthly", "Weekly", "Daily"])
        with colb:
            n = st.number_input("Number of Periods (n)", value=time * compute_factors(time_unit, comp_freq), disabled=True)

    colc, cold = st.columns(2)
    with colc:
        rate = st.number_input("Interest Rate/Time Unit (%)", min_value=0.0, value=5.0, step=.125)
    with cold:
        p_rate = st.number_input("Periodic Interest Rate (i) (%)", value=rate / compute_factors(time_unit, comp_freq), disabled=True)

    pv = npf.pv(p_rate/100, n, pmt, -fv)
    st.write(f"## Present Value: ${pv:,.2f}")

    # Save Scenario button
    if st.button("Save Scenario"):
        save_scenario("PV", {"fv": fv, "pmt": pmt, "rate": rate, "n": n, "time": time, "time_unit": time_unit, "comp_freq": comp_freq}, f"${pv:,.2f}")
        st.rerun()

    # Display PV scenarios
    display_scenarios("PV")


elif calculator == "Payment (PMT)":
    st.markdown("""Calculate the **Payment** required to achieve a future value or pay off a present value over a specified time period at a given interest rate.""")
    col1, col2 = st.columns(2)
    with col1:
        pv = st.number_input("Present Value (PV)", value=1000.0, step=50.0, icon=":material/attach_money:")
        cola, colb = st.columns(2)
        with cola:
            time = st.number_input("Time", min_value=0, value=10)
        with colb:
            time_unit = st.selectbox("Time Unit", ["Years", "Quarters", "Months", "Weeks", "Days"])

    with col2:
        fv = st.number_input("Future Value (FV)", value=0.0, step=50.0, icon=":material/attach_money:")
        cola, colb = st.columns(2)
        with cola:
            comp_freq = st.selectbox("Compounding Frequency", ["Annually", "Quarterly", "Monthly", "Weekly", "Daily"])
        with colb:
            n = st.number_input("Number of Periods (n)", value=time * compute_factors(time_unit, comp_freq), disabled=True)

    colc, cold = st.columns(2)
    with colc:
        rate = st.number_input("Interest Rate/Time Unit (%)", min_value=0.0, value=5.0, step=.125)
    with cold:
        p_rate = st.number_input("Periodic Interest Rate (i) (%)", value=rate / compute_factors(time_unit, comp_freq), disabled=True)

    pmt = npf.pmt(p_rate/100, n, -pv, fv)
    st.write(f"## Payment: ${pmt:,.2f}")

    # Save Scenario button
    if st.button("Save Scenario"):
        save_scenario("PMT", {"pv": pv, "fv": fv, "rate": rate, "n": n, "time": time, "time_unit": time_unit, "comp_freq": comp_freq}, f"${pmt:,.2f}")
        st.rerun()

    # Display PMT scenarios
    display_scenarios("PMT")

elif calculator == "Interest Rate (i)":
    st.markdown("""Calculate the **Interest Rate** required to achieve a future value or pay off a present value over a specified time period with given payments.""")
    col1, col2 = st.columns(2)
    with col1:
        pv = st.number_input("Present Value (PV)", value=1000.0, step=50.0, icon=":material/attach_money:")
        cola, colb = st.columns(2)
        with cola:
            time = st.number_input("Time", min_value=0, value=10)
        with colb:
            time_unit = st.selectbox("Time Unit", ["Years", "Quarters", "Months", "Weeks", "Days"])

    with col2:
        fv = st.number_input("Future Value (FV)", value=2000.0, step=50.0, icon=":material/attach_money:")
        cola, colb = st.columns(2)
        with cola:
            comp_freq = st.selectbox("Compounding Frequency", ["Annually", "Quarterly", "Monthly", "Weekly", "Daily"])
        with colb:
            n = st.number_input("Number of Periods (n)", value=time * compute_factors(time_unit, comp_freq), disabled=True)

    colc, cold = st.columns(2)
    with colc:
        pmt = st.number_input("Payment (PMT)", value=0.0, step=50.0, icon=":material/attach_money:")

    # Calculate the interest rate
    try:
        i_rate = npf.rate(n, pmt, pv, fv)
        st.write(f"## Interest Rate: {i_rate*100:,.2f}%")
    except:
        st.write("## Error: Could not calculate interest rate. Please check your inputs.")

    # Save Scenario button
    if st.button("Save Scenario"):
        save_scenario("I", {"pv": pv, "fv": fv, "pmt": pmt, "n": n, "time": time, "time_unit": time_unit, "comp_freq": comp_freq}, f"{i_rate*100:,.2f}%")
        st.rerun()

    # Display i scenarios
    display_scenarios("I")


elif calculator == "Time Period (n)":
    st.markdown("""Calculate the **Time Period** required to achieve a future value or pay off a present value with given payments and interest rate.""")
    col1, col2 = st.columns(2)
    with col1:
        pv = st.number_input("Present Value (PV)", value=-10000.0, step=50.0, icon=":material/attach_money:")
        pmt = st.number_input("Payment (PMT)", value=0.0, step=50.0, icon=":material/attach_money:")         

    with col2:
        fv = st.number_input("Future Value (FV)", value=100000.0, step=50.0, icon=":material/attach_money:") 
    
    cola, colb = st.columns(2)
    with cola:
        rate = st.number_input("Interest Rate/Time Unit (%)", min_value=0.0, value=8.0, step=.125)
    with colb:
        coli, colj = st.columns(2)
        with coli:
            time_unit = st.selectbox("Time Unit", ["Years", "Quarters", "Months", "Weeks", "Days"])
        with colj:    
            comp_freq = st.selectbox("Compounding Frequency", ["Annually", "Quarterly", "Monthly", "Weekly", "Daily"])
        p_rate = rate / compute_factors(time_unit, comp_freq)

    # Calculate the number of periods
    try:
        n = npf.nper(p_rate/100, pmt, pv, fv)
        # Convert periods back to the selected time unit
        time_factor = compute_factors(time_unit, comp_freq)
        n_time = n / time_factor
        st.write(f"## Time Period: {n_time:,.2f} {time_unit}")
        st.write(f"### Number of Periods (n): {n:,.2f}")
        
    except:
        st.write("## Error: Could not calculate time period. Please check your inputs.")

    # Save Scenario button
    if st.button("Save Scenario"):
        save_scenario("n", {"pv": pv, "fv": fv, "pmt": pmt, "rate": rate, "time_unit": time_unit, "comp_freq": comp_freq}, f"{n_time:,.2f} {time_unit}")
        st.rerun()

    # Display n scenarios
    display_scenarios("n")