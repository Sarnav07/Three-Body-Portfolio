import streamlit as st
import time
import json
import os

# Page Config
st.set_page_config(
    page_title="ThreeBodyPortfolio AI",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 Three-Body Portfolio: Mission Control")
st.markdown("### Autonomous AI Hedge Fund Agent")

# Sidebar
with st.sidebar:
    st.header("📡 Status Panel")
    if st.button('🔄 Force Refresh'):
        st.rerun()
    st.write("---")
    st.info("Network: Sepolia Testnet")
    st.write("Strategy: **Swarm Intelligence**")

# Auto-refresh mechanism (Every 2 seconds)
if 'last_update' not in st.session_state:
    st.session_state['last_update'] = 0

# LOAD REAL DATA
data_file = "frontend_layer/dashboard_state.json"
if os.path.exists(data_file):
    with open(data_file, "r") as f:
        data = json.load(f)
else:
    # Fallback if bot hasn't run yet
    data = {
        "timestamp": "Waiting...", "price": 0, "rsi": 50, "sentiment": "WAITING",
        "decision": "INIT", "agent": "System", "reason": "Waiting for first cycle...", "tx_hash": "N/A"
    }

# METRICS ROW
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="BTC Price", value=f"${data['price']:,.2f}")
with col2:
    st.metric(label="RSI (14)", value=f"{data['rsi']:.1f}")
with col3:
    color = "normal"
    if data['sentiment'] == "BULLISH": color = "off" # Greenish in Streamlit default
    st.metric(label="Market Sentiment", value=data['sentiment'])

st.divider()

# DECISION DISPLAY
st.subheader("🧠 Latest Neural Decision")

# Dynamic color based on decision
status_color = "gray"
if data['decision'] == "BUY": status_color = "green"
elif data['decision'] == "SELL": status_color = "red"
else: status_color = "blue"

with st.container(border=True):
    st.markdown(f"**Last Update:** {data['timestamp']}")
    st.markdown(f"### :{status_color}[{data['decision']}]")
    st.markdown(f"**Proposed by:** {data['agent']}")
    st.info(f"📝 **Reasoning:** {data['reason']}")
    
    if data['tx_hash'] != "N/A":
        st.success(f"🔗 **On-Chain Proof:** [{data['tx_hash'][:10]}...](https://sepolia.etherscan.io/tx/{data['tx_hash']})")
    else:
        st.caption("No transaction broadcast for this cycle.")

# Auto-rerun to keep data fresh
time.sleep(2)
st.rerun()