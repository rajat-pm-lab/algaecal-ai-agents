"""
Streamlit UI for CEO Chief of Staff Agent.
Run locally: streamlit run agents/ceo-chief-of-staff/app.py
"""

import sys
import os

# Add repo root and agent directory to path
_agent_dir = os.path.dirname(os.path.abspath(__file__))
_repo_root = os.path.join(_agent_dir, "..", "..")
sys.path.insert(0, os.path.abspath(_repo_root))
sys.path.insert(0, _agent_dir)

import streamlit as st
from datetime import date
from agent import build_context, generate_brief

st.set_page_config(page_title="CEO Daily Brief — AlgaeCal", page_icon="📊", layout="wide")

st.title("📊 CEO Daily Brief")
st.caption(f"AlgaeCal AI Chief of Staff · {date.today().strftime('%A, %B %d, %Y')}")

st.divider()

# Sidebar
with st.sidebar:
    st.header("Live Data Sources")
    st.success("Google Sheets — KPI Dashboard", icon="✅")
    st.success("Google Docs — CEO Weekly Update", icon="✅")
    st.info("Slack — Coming Soon", icon="⏳")
    st.info("HubSpot CRM — Coming Soon", icon="⏳")
    st.info("Notion — Coming Soon", icon="⏳")
    st.divider()
    show_raw = st.checkbox("Show raw data context", value=False)
    st.divider()
    st.markdown("**Agent:** CEO Chief of Staff")
    st.markdown("**LLM:** Model-agnostic (Gemini / Claude)")

# Generate brief
if st.button("🔄 Generate Today's Brief", type="primary", use_container_width=True):
    with st.spinner("Pulling live data from Google Sheets & Docs..."):
        try:
            brief = generate_brief()
            st.session_state["brief"] = brief
            st.session_state["context"] = build_context()
        except Exception as e:
            st.error(f"Error generating brief: {e}")

# Display brief
if "brief" in st.session_state:
    st.markdown(st.session_state["brief"])

    if show_raw and "context" in st.session_state:
        with st.expander("📋 Raw Data Context (sent to LLM)", expanded=False):
            st.markdown(st.session_state["context"])
else:
    st.info("Click **Generate Today's Brief** to pull live data from Google Sheets and Docs.")
