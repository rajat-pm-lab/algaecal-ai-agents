"""
Streamlit UI for CEO Chief of Staff Agent.
Run locally: streamlit run agents/ceo-chief-of-staff/app.py
"""

import sys
import os
import streamlit as st
from datetime import date

# Add repo root and agent directory to path
_agent_dir = os.path.dirname(os.path.abspath(__file__))
_repo_root = os.path.abspath(os.path.join(_agent_dir, "..", ".."))
if _repo_root not in sys.path:
    sys.path.insert(0, _repo_root)
if _agent_dir not in sys.path:
    sys.path.insert(0, _agent_dir)

st.set_page_config(page_title="CEO Daily Brief — AlgaeCal", page_icon="📊", layout="wide")

# Import agent after path setup — show errors in UI if it fails
try:
    from agent import build_context, generate_brief
    _import_error = None
except Exception as e:
    _import_error = e

st.title("📊 CEO Daily Brief")
st.caption(f"AlgaeCal AI Chief of Staff · {date.today().strftime('%A, %B %d, %Y')}")

if _import_error:
    st.error(f"Agent failed to load: {_import_error}")
    st.code(f"sys.path: {sys.path}\n\nRepo root: {_repo_root}\nAgent dir: {_agent_dir}")
    st.stop()

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
