import streamlit as st
import pandas as pd

def render():
    st.subheader("Exception Ledger (Audit Trail)")
    st.write("Transparent mathematical breakdown of flagged cohort risk scores.")
    
    audit_data = [
        {"Cohort ID": "cohort_1700_49.36.0.0", "Subnet Type": "CGNAT (Jio)", "Txn Count": 512, "SCI (Chi-Sq)": "3.12", "DenStream Density": "0.12 (Sparse)", "Action": "PASS"},
        {"Cohort ID": "cohort_1705_10.0.0.99", "Subnet Type": "Dedicated Proxy", "Txn Count": 34, "SCI (Chi-Sq)": "148.90", "DenStream Density": "0.94 (Dense)", "Action": "BLOCKED"},
        {"Cohort ID": "cohort_1710_192.168.1.0", "Subnet Type": "Residential", "Txn Count": 4, "SCI (Chi-Sq)": "N/A (N<30 Gate)", "DenStream Density": "0.05 (Sparse)", "Action": "SPEED LAYER ONLY"},
        {"Cohort ID": "cohort_1715_10.0.0.99", "Subnet Type": "Dedicated Proxy", "Txn Count": 48, "SCI (Chi-Sq)": "18.40 (Spoofed)", "DenStream Density": "0.98 (Dense)", "Action": "BLOCKED (Density Trigger)"}
    ]
    
    df = pd.DataFrame(audit_data)
    
    def color_action(val):
        if "BLOCKED" in str(val):
            return "background-color: #ffcccc; color: #900C3F; font-weight: bold;"
        elif "PASS" in str(val):
            return "background-color: #d4edda; color: #155724;"
        return "background-color: #fff3cd; color: #856404;"
        
    styled_df = df.style.applymap(color_action, subset=["Action"])
    st.dataframe(styled_df, use_container_width=True)