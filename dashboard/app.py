import streamlit as st
import requests
import time
import threading
import pandas as pd
from streamlit_autorefresh import st_autorefresh
from views import cluster_projection, cost_curve, monte_carlo_scaling, exception_ledger

st.set_page_config(page_title="RazorPulse", layout="wide")

st.markdown("""
    <style>
        .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
        .stButton>button { width: 100%; border-radius: 6px; height: 2.8rem; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

API_URL = "http://localhost:8000"

# --- SIDEBAR CONTROL PANEL ---
st.sidebar.header("⚙️ Command Center")

# SMOOTH LIVE SYNC: Uses JS to refresh every 2000ms without freezing Python
sync_active = st.sidebar.toggle("📡 Live API Sync", value=False, help="Smooth background refresh.")
if sync_active:
    st_autorefresh(interval=2000, limit=None, key="live_sync")

if st.sidebar.button("🧹 Reset System (Clear Ledger)"):
    requests.delete(f"{API_URL}/v1/telemetry/reset")
    st.sidebar.success("Backend memory cleared.")
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("**Simulation Controls:**")

# INSTANT BURST: Fires requests in a background thread to prevent UI freezing
if st.sidebar.button("🔴 Inject Adversarial Burst"):
    def inject_bot_traffic():
        for _ in range(40):
            try:
                requests.post(f"{API_URL}/v1/events/score/checkout", json={
                    "account_id": "bot-farm-999", "txn_id": f"txn-{time.time()}", 
                    "amount": 99.0, "ts": time.time(), "payment_instrument_hash": "stolen_hash", "ip_subnet": "10.0.0.99/24"
                })
            except:
                pass
    
    # Start the attack in the background
    threading.Thread(target=inject_bot_traffic, daemon=True).start()
    st.sidebar.error("🚨 Burst injected! It will appear on the next tick.")
    time.sleep(0.5) # Give the backend a fraction of a second to catch the first few requests
    st.rerun()

# --- FETCH LIVE STATE FROM BACKEND ---
try:
    response = requests.get(f"{API_URL}/v1/telemetry")
    telemetry_data = response.json().get("data", [])
    traffic_df = pd.DataFrame(telemetry_data)
except Exception as e:
    traffic_df = pd.DataFrame()
    st.sidebar.error("FastAPI Backend Offline")

# --- MAIN DASHBOARD ---
st.title("🛡️ RazorPulse: Synthetic Burst Detector")
st.markdown("<h4 style='color: #a0aec0; font-weight: 400; margin-top: -15px; margin-bottom: 20px;'>Enterprise-Grade Shield: Sub-millisecond spatial detection combined with autonomous post-mortem intelligence.</h4>", unsafe_allow_html=True)
st.markdown("---")

col_main, col_side = st.columns([2.2, 1])

with col_main:
    cluster_projection.render(traffic_df)
    st.markdown("---")
    col_bottom1, col_bottom2 = st.columns(2)
    with col_bottom1:
        cost_curve.render()
    with col_bottom2:
        monte_carlo_scaling.render()

with col_side:
    exception_ledger.render(traffic_df)