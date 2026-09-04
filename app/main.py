from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from collections import deque
import time
import numpy as np

app = FastAPI(title="RazorPulse Risk Engine API", version="1.2.0")

# --- IN-MEMORY STATE BUFFER ---
# In production, this would be Redis or TimescaleDB. 
# Here, we use a deque ring-buffer to store the last 500 telemetry points.
TELEMETRY_BUFFER = deque(maxlen=500)

# --- PYDANTIC SCHEMAS ---
class CheckoutPayload(BaseModel):
    account_id: str
    txn_id: str
    amount: float
    ts: float
    payment_instrument_hash: str
    ip_subnet: Optional[str] = "Residential (Default)"

class TelemetryResponse(BaseModel):
    status: str
    total_events: int
    data: List[Dict[str, Any]]

# --- CORE ENDPOINTS ---

@app.post("/v1/events/score/checkout")
async def score_checkout(payload: CheckoutPayload):
    """
    T-0 Speed Layer Endpoint: Ingests, scores, and stores a transaction.
    """
    # 1. Determine if this is an adversarial burst (Flaw 7) based on payload heuristics
    # In a fully wired ML backend, this routes through app.ml.denstream
    is_bot = "bot" in payload.account_id.lower() or payload.amount == 99.0
    
    # 2. Generate simulated spatial coordinates and scores for the Engine output
    if is_bot:
        traffic_type = "Flagged Burst"
        pca_1 = np.random.normal(loc=4.5, scale=0.15)
        pca_2 = np.random.normal(loc=4.5, scale=0.15)
        sci_score = round(np.random.uniform(90.0, 150.0), 2)
        subnet = "10.0.0.99/24 (Proxy)"
        action = "BLOCKED"
    else:
        traffic_type = "Legitimate"
        pca_1 = np.random.normal(loc=0, scale=1.5)
        pca_2 = np.random.normal(loc=0, scale=1.5)
        sci_score = round(np.random.uniform(1.0, 5.0), 2)
        subnet = payload.ip_subnet
        action = "PASS"

    # 3. Create the telemetry record exact schema expected by the frontend
    record = {
        "PCA Component 1": pca_1,
        "PCA Component 2": pca_2,
        "Traffic Type": traffic_type,
        "IP Subnet": subnet,
        "SCI Anomaly Score": sci_score,
        "Action": action,
        "Timestamp": time.time()
    }
    
    # 4. Append to the stateful ring-buffer
    TELEMETRY_BUFFER.append(record)

    # 5. Return the T-0 authorization decision
    return {
        "status": "success",
        "action": action,
        "risk_score": sci_score,
        "message": f"Transaction {action} in 42ms"
    }


@app.get("/v1/telemetry", response_model=TelemetryResponse)
async def get_telemetry():
    """
    Observability Endpoint: Serves the live state buffer to the Next.js/Streamlit dashboard.
    """
    return {
        "status": "live",
        "total_events": len(TELEMETRY_BUFFER),
        "data": list(TELEMETRY_BUFFER)
    }

@app.delete("/v1/telemetry/reset")
async def reset_telemetry():
    """Clears the buffer (Useful for resetting the demo)."""
    TELEMETRY_BUFFER.clear()
    return {"status": "cleared"}