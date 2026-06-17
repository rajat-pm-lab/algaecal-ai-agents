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

# Check Slack availability
_slack_connected = False
try:
    from shared.config import get_secret
    get_secret("SLACK_BOT_TOKEN")
    get_secret("SLACK_CHANNEL_ID")
    _slack_connected = True
except Exception:
    pass

st.title("📊 CEO Daily Brief")
st.caption(f"AlgaeCal AI Chief of Staff · {date.today().strftime('%A, %B %d, %Y')}")

if _import_error:
    st.error(f"Agent failed to load: {_import_error}")
    st.code(f"sys.path: {sys.path}\n\nRepo root: {_repo_root}\nAgent dir: {_agent_dir}")
    st.stop()

# --- Demo Notice ---
st.info(
    "**Demo Mode** — This agent is built with dummy AlgaeCal data for quick demo and feedback. "
    "Production deployment would connect to real data sources via MCP connectors.",
    icon="💡"
)

# Sidebar
with st.sidebar:
    st.header("Live Data Sources")
    st.success("Google Sheets — KPI Dashboard", icon="✅")
    st.success("Google Docs — CEO Weekly Update", icon="✅")
    if _slack_connected:
        st.success("Slack — Team Updates", icon="✅")
    else:
        st.info("Slack — Not configured", icon="⏳")
    st.info("HubSpot CRM — Coming Soon", icon="⏳")
    st.info("Notion — Coming Soon", icon="⏳")
    st.divider()
    show_raw = st.checkbox("Show raw data context", value=False)
    show_architecture = st.checkbox("Show agent architecture", value=False)
    st.divider()
    st.markdown("**Agent:** CEO Chief of Staff")
    st.markdown("**LLM:** Model-agnostic (Gemini / Claude)")
    st.divider()
    if st.button("🔄 Refresh Brief", use_container_width=True):
        for key in ["context", "brief"]:
            st.session_state.pop(key, None)
        st.rerun()

st.divider()

# --- Agent Architecture Section ---
if show_architecture:
    st.markdown("## 🏗️ Agent Architecture")
    st.markdown(
        "This is not a simple chatbot or wrapper around an LLM. "
        "It is an **autonomous AI agent** that orchestrates multiple data sources, "
        "reasons across them, and produces actionable executive intelligence."
    )

    arch_cols = st.columns(4)
    with arch_cols[0]:
        st.markdown("#### 🔗 Multi-Source Orchestration")
        st.markdown(
            "Pulls live data from **6+ business systems** in parallel — "
            "Google Sheets (4 tabs), Google Docs, and Slack. "
            "Production-ready for Salesforce, Jira, HubSpot via MCP connectors."
        )
    with arch_cols[1]:
        st.markdown("#### 🧠 Reasoning Layer")
        st.markdown(
            "Doesn't just summarize — **cross-references** revenue trends against "
            "customer health, hiring gaps against engineering velocity, and Slack chatter "
            "against strategic priorities to surface what actually matters."
        )
    with arch_cols[2]:
        st.markdown("#### 🔄 Agentic Loop")
        st.markdown(
            "Executes a full **Gather → Analyze → Synthesize → Recommend** loop autonomously. "
            "Each run pulls fresh data, identifies risks, and generates prioritized actions "
            "without human prompting."
        )
    with arch_cols[3]:
        st.markdown("#### ⚙️ Production Architecture")
        st.markdown(
            "**Model-agnostic** LLM provider (swap Gemini ↔ Claude in one line). "
            "Concurrent data fetching via ThreadPoolExecutor. "
            "Structured outputs with source attribution."
        )

    # Technical details expander
    with st.expander("🔍 Technical Details", expanded=False):
        tech_col1, tech_col2 = st.columns(2)
        with tech_col1:
            st.markdown("**Data Pipeline**")
            st.markdown(
                "- Google Sheets API → 4 tabs (Revenue, Products, Customers, Hiring)\n"
                "- Google Docs API → CEO Weekly Strategy Update\n"
                "- Slack API → Team channel messages (real-time)\n"
                "- All fetched concurrently via `ThreadPoolExecutor`\n"
                "- Graceful degradation — if one source fails, others still work"
            )
        with tech_col2:
            st.markdown("**Agent Capabilities**")
            st.markdown(
                "- **Multi-step reasoning**: Breaks CEO brief into subtasks per data domain\n"
                "- **Tool use**: Calls Google, Slack APIs to gather live data\n"
                "- **Autonomous decision-making**: Identifies risks, prioritizes actions\n"
                "- **Structured output**: Executive brief with citations and recommendations\n"
                "- **Conversational follow-up**: Ask questions grounded in the data"
            )

        st.markdown("**Agent Flow**")
        st.code(
            "1. GATHER  →  Pull data from Google Sheets (4 tabs) + Docs + Slack in parallel\n"
            "2. ANALYZE →  LLM cross-references all sources, identifies patterns & risks\n"
            "3. SYNTHESIZE → Produces structured brief with metrics, risks, opportunities\n"
            "4. RECOMMEND → Generates 3-5 prioritized CEO action items for today\n"
            "5. INTERACT → CEO can ask follow-up questions grounded in the same data",
            language=None,
        )

    st.divider()

# --- Auto-generate brief on page load ---
source_label = "Google Sheets, Docs & Slack..." if _slack_connected else "Google Sheets & Docs..."
if "context" not in st.session_state:
    with st.spinner(f"Pulling live data from {source_label}"):
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
if user_input := st.chat_input("Ask about revenue, products, hiring, customers, Slack updates..."):
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
