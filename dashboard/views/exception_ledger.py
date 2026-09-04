import streamlit as st
import pandas as pd
from agents.swarm import run_investigation 

def render(df):
    # --- DYNAMIC DATA AGGREGATION ---
    if df is not None and not df.empty:
        summary_df = df.groupby('IP Subnet').agg(
            Txns=('Action', 'count'),
            Density=('SCI Anomaly Score', 'max'),
            Action=('Action', lambda x: 'BLOCKED' if 'BLOCKED' in x.values else 'PASS')
        ).reset_index()
        summary_df.rename(columns={'IP Subnet': 'Target Subnet'}, inplace=True)
    else:
        summary_df = pd.DataFrame(columns=['Target Subnet', 'Txns', 'Density', 'Action'])

    blocked_df = summary_df[summary_df['Action'] == "BLOCKED"]
    blocked_ids = blocked_df['Target Subnet'].tolist()

    # --- TOP: AUTONOMOUS RISK INVESTIGATION ---
    st.subheader("🧠 Autonomous Risk Investigation")
    st.write("Deploy the Agentic Swarm to investigate blocked events.")
    
    if not blocked_ids:
        st.info("No blocked cohorts detected. Inject a burst to generate an exception.")
    else:
        target_cohort = st.selectbox("Select Blocked Target:", blocked_ids)
        
        if st.button("🚀 Deploy Agent Swarm", use_container_width=True):
            target_data = blocked_df[blocked_df['Target Subnet'] == target_cohort].iloc[0]
            
            with st.expander("Terminal: Swarm Execution Logs", expanded=True):
                terminal_placeholder = st.empty()
                log_text = ""
                final_intel = ""
                final_risk = ""
                final_comms = ""
                
                # We capture the specific outputs from the generator
                for chunk in run_investigation(target_cohort, target_cohort, target_data['Density']):
                    log_text += chunk
                    terminal_placeholder.markdown(log_text)
                    
                    # Exact string matching based on the swarm.py outputs
                    if "🔍 **[IntelAgent Output]**:" in chunk:
                        final_intel = chunk.split("🔍 **[IntelAgent Output]**:")[1].strip()
                    if "📊 **[RiskQuantAgent Output]**:" in chunk:
                        final_risk = chunk.split("📊 **[RiskQuantAgent Output]**:")[1].strip()
                    if "✉️ **[CommsAgent Final Report]**:" in chunk:
                        final_comms = chunk.split("✉️ **[CommsAgent Final Report]**:")[1].strip()
                        
            st.success("Post-Mortem Report Generated Dynamically by AI.")
            
            # --- NATIVE STREAMLIT UI INJECTED WITH REAL AI DATA ---
            with st.container(border=True):
                st.markdown("### 🛡️ Automated Risk Post-Mortem")
                st.markdown(f"**Tracking Target:** `{target_cohort}` &nbsp;|&nbsp; **Status:** 🟢 **CONTAINED**")
                
                st.divider()
                
                st.markdown("#### 🔬 Technical Threat Intelligence (IntelAgent)")
                st.markdown(f"> {final_intel if final_intel else 'Intelligence data unavailable.'}")
                
                st.markdown("#### 💼 Financial Exposure (RiskQuantAgent)")
                st.markdown(f"> {final_risk if final_risk else 'Financial calculation unavailable.'}")
                
                st.markdown("#### ✉️ Merchant Advisory (CommsAgent)")
                st.markdown(f"> {final_comms if final_comms else 'Advisory drafting failed.'}")
                
                st.divider()
                
                st.markdown("#### ⚡ Automated Mitigations Applied")
                st.markdown(f"- Gateway-level drop implemented for {target_data['Txns']} unique synthetic device hashes.")
                st.markdown("- Dynamic 3D-Secure (OTP) step-up enforced for all adjacent carts > ₹10,000.")
                
                st.info("🎯 **Recommended Next Actions (Risk Ops)**")
                st.checkbox("Auto-drafted incident email ready for Merchant approval.", value=True, disabled=True)
                st.checkbox(f"Escalate proxy subnet {target_cohort} to Global Network Blocklist.")
                st.checkbox("Run historical sweep for dormant accounts sharing these device hashes.")
            
    st.markdown("---")

    # --- BOTTOM: EXCEPTION LEDGER ---
    st.subheader("Live Exception Ledger")
    def color_action(val):
        if "BLOCKED" in str(val): return "background-color: #ffcccc; color: #900C3F; font-weight: bold;"
        elif "PASS" in str(val): return "background-color: #d4edda; color: #155724;"
        return "background-color: #fff3cd; color: #856404;"
        
    styled_df = summary_df.style.map(color_action, subset=["Action"])
    st.dataframe(styled_df, use_container_width=True, hide_index=True)