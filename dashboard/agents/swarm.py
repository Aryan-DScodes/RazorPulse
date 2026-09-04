import time

def run_investigation(cohort_id, subnet_type, risk_score):
    """
    Generator function simulating a Multi-Agent LLM Swarm investigation.
    Yields chunks of text to stream into a Streamlit terminal UI.
    """
    yield "⚙️ **[Orchestrator]** T-0 Block event received. Initializing T+1 Agentic Swarm...\n\n"
    time.sleep(1.0)
    
    # --- AGENT 1: INTEL ---
    yield f"🔍 **[IntelAgent]** Taking ownership of target: `{cohort_id}` ({subnet_type}). Querying global OSINT and dark-web telemetry...\n"
    time.sleep(1.5)
    yield "🔍 **[IntelAgent]** 🚨 CRITICAL MATCH: Subnet recognized as a known high-speed proxy network associated with the 'Scattered Spider' syndicate. Extracting 48 unique synthetic browser fingerprints.\n\n"
    time.sleep(1.0)

    # --- AGENT 2: RISK QUANT ---
    yield f"📊 **[RiskQuantAgent]** Ingesting Intel payload. Cross-referencing merchant historicals (Category: Electronics) and DenStream density score ({risk_score})...\n"
    time.sleep(1.5)
    yield "📊 **[RiskQuantAgent]** ⚠️ EXPOSURE CALCULATED: Attack vector aligns with automated credential stuffing aimed at high-value inventory. Immediate financial blast radius estimated at **₹4,50,000**. Recommending aggressive 3D-Secure step-up.\n\n"
    time.sleep(1.0)

    # --- AGENT 3: COMMS ---
    yield "✉️ **[CommsAgent]** Translating technical forensics into merchant advisory payload. Drafting Incident Report...\n"
    time.sleep(1.5)
    yield "✉️ **[CommsAgent]** ✅ Action complete. 3D-Secure policies dynamically updated via webhook. Report generated for Merchant dashboard.\n"