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

# Import agent after path setup
try:
    from agent import build_context, generate_brief, chat_with_context
    _import_error = None
except Exception as e:
    _import_error = e

st.title("📊 CEO Daily Brief")
st.caption(f"AlgaeCal AI Chief of Staff · {date.today().strftime('%A, %B %d, %Y')}")

if _import_error:
    st.error(f"Agent failed to load: {_import_error}")
    st.code(f"sys.path: {sys.path}\n\nRepo root: {_repo_root}\nAgent dir: {_agent_dir}")
    st.stop()

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
    st.divider()
    if st.button("🔄 Refresh Brief", use_container_width=True):
        for key in ["context", "brief"]:
            st.session_state.pop(key, None)
        st.rerun()

st.divider()

# --- Auto-generate brief on page load ---
if "context" not in st.session_state:
    with st.spinner("Pulling live data from Google Sheets & Docs..."):
        try:
            st.session_state["context"] = build_context()
        except Exception as e:
            st.error(f"Error fetching data: {e}")
            st.stop()

if "brief" not in st.session_state:
    with st.spinner("Generating today's brief..."):
        try:
            st.session_state["brief"] = generate_brief(context=st.session_state["context"])
        except Exception as e:
            st.error(f"⚠️ Could not generate brief right now. This is usually a temporary API issue — click **Refresh Brief** in the sidebar to try again.")
            st.stop()

# Display brief
st.markdown(st.session_state["brief"])

if show_raw:
    with st.expander("📋 Raw Data Context (sent to LLM)", expanded=False):
        st.markdown(st.session_state["context"])

# --- Ask Your Algae Bud (sticky at bottom via Streamlit's native chat_input) ---
st.divider()
st.markdown("### 🌿 Ask Your Algae Bud")
st.caption("Ask follow-up questions — answers come strictly from your connected data sources.")

# Initialize chat history
if "chat_messages" not in st.session_state:
    st.session_state["chat_messages"] = []

# Display chat history in a scrollable container
chat_container = st.container()
with chat_container:
    for msg in st.session_state["chat_messages"]:
        with st.chat_message(msg["role"], avatar="🧑‍💼" if msg["role"] == "user" else "🌿"):
            st.markdown(msg["content"])

# Chat input — Streamlit pins this to the bottom of the viewport automatically
if user_input := st.chat_input("Ask about revenue, products, hiring, customers..."):
    st.session_state["chat_messages"].append({"role": "user", "content": user_input})
    with chat_container:
        with st.chat_message("user", avatar="🧑‍💼"):
            st.markdown(user_input)

        with st.chat_message("assistant", avatar="🌿"):
            with st.spinner("Thinking..."):
                try:
                    response = chat_with_context(
                        user_message=user_input,
                        context=st.session_state["context"],
                        chat_history=st.session_state["chat_messages"][:-1],
                    )
                    st.markdown(response)
                    st.session_state["chat_messages"].append({"role": "assistant", "content": response})
                except Exception as e:
                    st.warning(
                        "⚠️ Couldn't get a response right now — the AI service may be temporarily busy. "
                        "Try again in a few seconds."
                    )
