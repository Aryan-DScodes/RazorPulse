import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

def render():
    st.subheader("Cohort Density Projection (PCA)")
    st.write("Visualizing the DenStream feature space. Red clusters indicate synthetic coordination.")
    
    # --- MOCK DATA GENERATOR FOR UI MVP ---
    np.random.seed(42)
    
    # 1. Baseline human traffic (diffuse, natural variance)
    base_x = np.random.normal(loc=0, scale=1.5, size=150)
    base_y = np.random.normal(loc=0, scale=1.5, size=150)
    
    # 2. Adversarial Bot Burst (tightly clustered due to shared scripts/IPs)
    bot_x = np.random.normal(loc=4.5, scale=0.15, size=30)
    bot_y = np.random.normal(loc=4.5, scale=0.15, size=30)
    
    # Combine into a Pandas DataFrame
    df = pd.DataFrame({
        "PCA Component 1": np.concatenate([base_x, bot_x]),
        "PCA Component 2": np.concatenate([base_y, bot_y]),
        "Traffic Type": ["Legitimate"] * 150 + ["Flagged Burst"] * 30,
        "IP Subnet": ["Varied"] * 150 + ["10.0.0.99/24"] * 30,
        "SCI Anomaly Score": np.random.uniform(1.0, 5.0, 150).tolist() + np.random.uniform(90.0, 150.0, 30).tolist()
    })
    
    # --- PLOTLY INTERACTIVE CHART ---
    fig = px.scatter(
        df, 
        x="PCA Component 1", 
        y="PCA Component 2", 
        color="Traffic Type",
        color_discrete_map={"Legitimate": "#3498db", "Flagged Burst": "#e74c3c"},
        hover_data={"IP Subnet": True, "SCI Anomaly Score": ':.2f'}
    )
    
    # Strip unnecessary margins for a cleaner dashboard look
    fig.update_layout(
        margin=dict(l=0, r=0, t=10, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    # Render the chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)