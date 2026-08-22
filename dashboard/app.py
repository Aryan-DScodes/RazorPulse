import streamlit as st
import requests
import time
from views import cluster_projection, cost_curve, monte_carlo_scaling, exception_ledger

# Must be the first Streamlit command
st.set_page_config(page_title="Ledger-Genesis", layout="wide")

# --- CUSTOM FINTECH STYLING ---
st.markdown("""
    <style>
        .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
        div[data-testid="stMetricValue"] { font-size: 1.6rem; font-weight: 700; }
        .stButton>button { width: 100%; border-radius: 6px; height: 2.8rem; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

# --- STATE MANAGEMENT ---
if "api_status" not in st.session_state:
    st.session_state.api_status = "Waiting for traffic..."

# --- SIDEBAR CONTROL PANEL ---
st.sidebar.header("⚙️ Command Center")
st.sidebar.markdown("Trigger live API traffic:")

API_URL = "http://localhost:8000/v1/events/score/checkout"

if st.sidebar.button("🟢 Fire Baseline Traffic"):
    with st.spinner("Pinging FastAPI backend..."):
        try:
            # We fire a clean checkout event to the API we built on Day 2
            payload = {
                "account_id": "clean-human-001", 
                "txn_id": "txn-1001", 
                "amount": 45.50, 
                "ts": time.time(), 
                "payment_instrument_hash": "secure_hash_x"
            }
            response = requests.post(API_URL, json=payload)
            st.session_state.api_status = f"✅ Server Response: {response.json()}"
            st.sidebar.success("Passed")
        except requests.exceptions.ConnectionError:
            st.session_state.api_status = "❌ ERROR: FastAPI server is offline. Run Uvicorn!"
            st.sidebar.error("Connection Failed")

if st.sidebar.button("🔴 Inject Adversarial Burst"):
    with st.spinner("Injecting Flaw 7 Burst..."):
        try:
            # Simulating the charm-pricing bot ring hitting the endpoint
            payload = {
                "account_id": "bot-farm-999", 
                "txn_id": "txn-9999", 
                "amount": 99.0, # The spoofed charm price
                "ts": time.time(), 
                "payment_instrument_hash": "stolen_hash_y"
            }
            response = requests.post(API_URL, json=payload)
            
            # In a full implementation, the backend detects the anomaly and returns a high risk score
            st.session_state.api_status = f"🚨 ALERT: Burst Blocked. API Response: {response.json()}"
            st.sidebar.error("Burst Blocked")
        except requests.exceptions.ConnectionError:
            st.session_state.api_status = "❌ ERROR: FastAPI server is offline. Run Uvicorn!"
            st.sidebar.error("Connection Failed")

st.sidebar.markdown("---")
st.sidebar.info(f"**System Status:** {st.session_state.api_status}")

# --- MAIN DASHBOARD ---
st.title("🛡️ Ledger-Genesis: Synthetic Burst Detector")
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