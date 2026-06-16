"""
Streamlit UI for CEO Chief of Staff Agent.
Run: streamlit run agents/ceo-chief-of-staff/app.py
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import streamlit as st
from datetime import date
from agent import build_context, generate_brief

st.set_page_config(page_title="CEO Daily Brief — AlgaeCal", page_icon="📊", layout="wide")

st.title("📊 CEO Daily Brief")
st.caption(f"AlgaeCal AI Chief of Staff · {date.today().strftime('%A, %B %d, %Y')}")

st.divider()

# Sidebar with raw data toggle
with st.sidebar:
    st.header("Controls")
    show_raw = st.checkbox("Show raw data context", value=False)
    st.divider()
    st.markdown("**Agent:** CEO Chief of Staff")
    st.markdown("**Data sources:** Revenue KPIs, Customers, Escalations, Engineering, Hiring, Slack")
    st.markdown("**LLM:** Model-agnostic (Gemini / Claude)")

# Generate brief
if st.button("🔄 Generate Today's Brief", type="primary", use_container_width=True):
    with st.spinner("Pulling company data and generating brief..."):
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
    st.info("Click **Generate Today's Brief** to pull the latest company data and produce the CEO daily brief.")
