import streamlit as st
import pandas as pd

def render():
    st.subheader("Exception Ledger (Audit Trail)")
    st.write("System does not auto-block without a traceable reason.")
    
    # Mock data for the final presentation
    data = {
        "Cohort ID": ["cohort_1700_49.36", "cohort_1715_10.0"],
        "SCI Score": [8.4, 142.1],
        "Cluster Density": ["Sparse", "Dense"],
        "Detection Lag (s)": [0, 42],
        "Action": ["Pass", "Blocked"]
    }
    st.dataframe(pd.DataFrame(data))