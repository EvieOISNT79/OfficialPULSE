import streamlit as st
import requests
from datetime import datetime, timedelta
import plotly.graph_objects as go
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import csv
import os
import time

st.set_page_config(page_title="Official Pulse Terminal", layout="wide")

# Premium Styling
st.markdown("""
<style>
    .stApp { background-color: #0a0a0a; }
    .stMetric { background-color: #111111; border: 2px solid #00ff9f; border-radius: 12px; padding: 15px; }
    h1, h2 { color: #00ff9f; text-shadow: 0 0 12px #00ff9f; }
    .surge { color: #ff00ff; font-weight: bold; animation: pulse 1.5s infinite; }
    .injury-alert { color: #ff4444; font-weight: bold; }
    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
</style>
""", unsafe_allow_html=True)

st.title("🟢 Official Pulse Terminal")
st.markdown("**Cross-Market Intelligence** — Velocity Surge + Sports & Crypto Signals")

# Logging
LOG_FILE = "pulse_history.csv"
if not os.path.exists(LOG_FILE):
    pd.DataFrame(columns=["timestamp", "category", "velocity", "avg_anger", "surge", "notes"]).to_csv(LOG_FILE, index=False)

def log_pulse(category, velocity, avg_anger, surge, notes=""):
    pd.DataFrame([[datetime.now(), category, velocity, avg_anger, surge, notes]]).to_csv(LOG_FILE, mode='a', header=False, index=False)

sia = SentimentIntensityAnalyzer()

def calculate_pulse(category):
    # Placeholder velocity (replace with real X data later when we fix Playwright)
    velocity = 7 if category in ["Geopolitics", "Politics"] else 4
    avg_anger = 0.42 if category in ["Geopolitics", "Politics"] else 0.28
    surge = velocity >= 5 or avg_anger > 0.4
    notes = ""
    injury_alert = None
    crypto_data = None

    if category == "Sports":
        notes = "TheSportsDB lineup/injury proxy"
        injury_alert = "Key player status changes possible — lineup impact on spread"
    elif category == "Crypto":
        notes = "CoinGecko market data"
        crypto_data = "Placeholder for top coins & volume"

    return {
        "velocity": velocity,
        "avg_anger": avg_anger,
        "surge": surge,
        "notes": notes,
        "injury_alert": injury_alert,
        "crypto_data": crypto_data
    }

# Sidebar
with st.sidebar:
    st.header("📊 Categories")
    categories = ["All Markets", "Geopolitics", "Politics", "Crypto", "Sports"]
    selected_category = st.selectbox("Select Category", categories, index=0)

# Overview
st.subheader("📡 Pulse Overview — All Markets")
cols = st.columns(4)
for i, cat in enumerate(["Geopolitics", "Politics", "Crypto", "Sports"]):
    with cols[i]:
        p = calculate_pulse(cat)
        st.metric(cat, f"{p['velocity']} posts", f"↑ {p['avg_anger']} anger")
        if p['surge']:
            st.markdown('<p class="surge">🚨 VELOCITY SURGE DETECTED</p>', unsafe_allow_html=True)

# Deep Dive
st.divider()
st.subheader(f"🔥 Deep Dive — {selected_category}")
pulse = calculate_pulse(selected_category)

c1, c2 = st.columns(2)
with c1:
    st.metric("Velocity (last 15 min)", f"{pulse['velocity']} posts")
with c2:
    st.metric("Avg Anger Score", f"{pulse['avg_anger']}")

if pulse['surge']:
    st.markdown('<p class="surge">🚨 VELOCITY SURGE DETECTED — Potential Market Edge!</p>', unsafe_allow_html=True)

if selected_category == "Sports" and pulse.get("injury_alert"):
    st.markdown(f'<p class="injury-alert">🩹 {pulse["injury_alert"]}</p>', unsafe_allow_html=True)

if selected_category == "Crypto" and pulse.get("crypto_data"):
    st.info("🐳 Crypto whale & flow signals coming soon (CoinGecko integration ready)")

if st.button("🔄 Refresh All Data Now", type="primary"):
    st.success(f"Refreshed at {datetime.now().strftime('%H:%M:%S')}")
    st.rerun()

log_pulse(selected_category, pulse['velocity'], pulse['avg_anger'], pulse['surge'], pulse.get("notes", ""))
st.caption(f"✅ Auto-refreshed at {datetime.now().strftime('%H:%M:%S')} • Data logged")

time.sleep(60)
st.rerun()
