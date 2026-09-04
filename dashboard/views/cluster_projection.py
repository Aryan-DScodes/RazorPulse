import streamlit as st
import plotly.express as px

def render(df):
    st.subheader("Cohort Density Projection (PCA)")
    st.write("Visualizing the DenStream feature space. Red clusters indicate synthetic coordination.")
    
    if df is None or df.empty:
        st.info("📡 Awaiting live traffic stream from API...")
        return
        
    fig = px.scatter(
        df, 
        x="PCA Component 1", 
        y="PCA Component 2", 
        color="Traffic Type",
        color_discrete_map={"Legitimate": "#3498db", "Flagged Burst": "#e74c3c"},
        hover_data={"IP Subnet": True, "SCI Anomaly Score": ':.2f'}
    )
    
    fig.update_layout(
        height=500,
        margin=dict(l=0, r=0, t=10, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(range=[-5, 7]), 
        yaxis=dict(range=[-5, 7])
    )
    
    st.plotly_chart(fig, use_container_width=True)