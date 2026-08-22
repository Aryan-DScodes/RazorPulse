import streamlit as st

def render():
    st.subheader("Cohort Density Projection (PCA)")
    st.write("Visualizing the DenStream feature space. Red dots represent flagged tight-density bot rings.")
    # In reality, you would pass your cluster coordinates to st.scatter_chart()
    st.info("Scatter Plot: [ Legitimate Traffic (Blue) vs. Injected Burst (Red) ]")