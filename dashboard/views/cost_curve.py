import streamlit as st
import plotly.graph_objects as go
import numpy as np

def render():
    st.subheader("Financial Optimization Sweep")
    st.write("Calculates total Rupee (₹) cost across discrimination thresholds using the cost equation.")
    
    thresholds = np.linspace(0.1, 0.95, 50)
    # Simulated financial cost curve based on c_FP and c_FN formulas
    fp_costs = 50000 * (1 - thresholds)**2.5
    fn_costs = 80000 * (thresholds)**3
    total_costs = fp_costs + fn_costs
    
    optimal_idx = np.argmin(total_costs)
    opt_thresh = thresholds[optimal_idx]
    min_cost = total_costs[optimal_idx]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=thresholds, y=fp_costs, mode='lines', name='False Positive Friction (c_FP)', line=dict(dash='dash', color='#e67e22')))
    fig.add_trace(go.Scatter(x=thresholds, y=fn_costs, mode='lines', name='False Negative Bleed (c_FN)', line=dict(dash='dash', color='#e74c3c')))
    fig.add_trace(go.Scatter(x=thresholds, y=total_costs, mode='lines', name='Total Expected Loss (₹)', line=dict(color='#2ecc71', width=3)))
    
    fig.add_vline(x=opt_thresh, line_width=2, line_dash="dot", line_color="#3498db", annotation_text=f"Optimal: {opt_thresh:.2f}")
    
    fig.update_layout(
        height=300, # Added explicit height
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis_title="Score Threshold",
        yaxis_title="Expected Loss (₹)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.metric(label="Optimal Operating Threshold", value=f"{opt_thresh:.2f}", delta=f"Min Loss: ₹{min_cost:,.0f}")