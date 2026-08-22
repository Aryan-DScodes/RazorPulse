import streamlit as st
from views import cluster_projection, cost_curve, monte_carlo_scaling, exception_ledger

st.set_page_config(page_title="Ledger-Genesis", layout="wide")

st.title("Ledger-Genesis: Synthetic Burst Detector")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    cluster_projection.render()
    st.markdown("---")
    cost_curve.render()

with col2:
    monte_carlo_scaling.render()
    st.markdown("---")
    exception_ledger.render()