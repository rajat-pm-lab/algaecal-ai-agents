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

ALGAECAL_LOGO = "https://cdn.shopify.com/s/files/1/0911/6041/2476/files/AlgaeCal-default-no-copyright.svg"

st.set_page_config(page_title="CEO Daily Brief — AlgaeCal", page_icon="🦴", layout="wide")

# --- AlgaeCal Brand CSS ---
st.markdown("""
<style>
    /* Header bar */
    header[data-testid="stHeader"] {
        background-color: #013b30;
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #013b30;
    }
    section[data-testid="stSidebar"] * {
        color: #f2f6f5 !important;
    }
    section[data-testid="stSidebar"] .stCheckbox label span {
        color: #f2f6f5 !important;
    }

    /* Sidebar logo — invert dark green SVG to white */
    section[data-testid="stSidebar"] img {
        filter: brightness(0) invert(1) !important;
    }

    /* Brand green buttons */
    .stButton > button {
        background-color: #013b30;
        color: white;
        border: none;
        border-radius: 8px;
    }
    .stButton > button:hover {
        background-color: #025c4a;
        color: white;
    }

    /* Info boxes */
    div[data-testid="stAlert"] {
        border-radius: 8px;
    }

    /* Chat input styling */
    .stChatInput > div {
        border-color: #013b30;
    }

    /* Architecture cards */
    .arch-card {
        background: #f2f6f5;
        border-left: 4px solid #013b30;
        padding: 1.2rem;
        border-radius: 8px;
        height: 100%;
    }
    .arch-card h4 {
        color: #013b30;
        margin-top: 0;
    }

    /* Expander headers */
    details summary {
        color: #013b30 !important;
    }

    /* Dividers */
    hr {
        border-color: #e0e8e5;
    }

    /* --- Daily Brief readability --- */
    .brief-container {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        font-size: 1rem;
        line-height: 1.7;
        color: #222222;
    }
    .brief-container h1, .brief-container h2, .brief-container h3,
    .brief-container h4, .brief-container h5, .brief-container h6 {
        color: #013b30;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }
    .brief-container h2 { font-size: 1.4rem; }
    .brief-container h3 { font-size: 1.2rem; }
    .brief-container strong { color: #013b30; }
    .brief-container ul, .brief-container ol {
        padding-left: 1.5rem;
        margin-bottom: 0.8rem;
    }
    .brief-container li {
        margin-bottom: 0.4rem;
        line-height: 1.6;
    }
    .brief-container code {
        font-size: 0.95rem;
        background: #f2f6f5;
        padding: 0.1rem 0.4rem;
        border-radius: 4px;
    }
    .brief-container p {
        margin-bottom: 0.6rem;
    }

    /* --- Sticky chat bar at bottom --- */
    .sticky-chat-header {
        position: fixed;
        bottom: 68px;
        left: 0;
        right: 0;
        background: white;
        padding: 0.5rem 2rem;
        border-top: 2px solid #013b30;
        z-index: 999;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .sticky-chat-header span.label {
        font-size: 1rem;
        font-weight: 600;
        color: #013b30;
    }
    .sticky-chat-header span.sublabel {
        font-size: 0.8rem;
        color: #6a6b6e;
    }

    /* Push Streamlit's native chat_input bar styling */
    .stChatInput {
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        right: 0 !important;
        padding: 0.75rem 2rem !important;
        background: white !important;
        border-top: 1px solid #e0e8e5 !important;
        z-index: 1000 !important;
    }

    /* Add padding at bottom of main content so it doesn't hide behind sticky bar */
    .main .block-container {
        padding-bottom: 140px !important;
    }
</style>
""", unsafe_allow_html=True)

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

# --- Header with Logo ---
st.image(ALGAECAL_LOGO, width=160)
st.markdown(
    f"<h1 style='margin-top: 0; color: #013b30;'>CEO Daily Brief</h1>"
    f"<p style='color: #6a6b6e; margin-top: -0.8rem;'>AI Chief of Staff Agent · {date.today().strftime('%A, %B %d, %Y')}</p>",
    unsafe_allow_html=True,
)

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
    st.image(ALGAECAL_LOGO, width=160)
    st.markdown("---")
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
    st.markdown(
        "<div style='text-align:center; font-size:0.75rem; opacity:0.7;'>"
        "Built by Rajat Singh<br>AI Product Builder Portfolio"
        "</div>",
        unsafe_allow_html=True,
    )

st.divider()

# --- Agent Architecture Section ---
if show_architecture:
    st.markdown("## Agent Architecture")
    st.markdown(
        "This is not a simple chatbot or wrapper around an LLM. "
        "It is an **autonomous AI agent** that orchestrates multiple data sources, "
        "reasons across them, and produces actionable executive intelligence."
    )

    arch_cols = st.columns(4)
    with arch_cols[0]:
        st.markdown(
            '<div class="arch-card">'
            "<h4>🔗 Multi-Source Orchestration</h4>"
            "<p>Pulls live data from <strong>6+ business systems</strong> in parallel — "
            "Google Sheets (4 tabs), Google Docs, and Slack. "
            "Production-ready for Salesforce, Jira, HubSpot via MCP connectors.</p>"
            "</div>",
            unsafe_allow_html=True,
        )
    with arch_cols[1]:
        st.markdown(
            '<div class="arch-card">'
            "<h4>🧠 Reasoning Layer</h4>"
            "<p>Doesn't just summarize — <strong>cross-references</strong> revenue trends against "
            "customer health, hiring gaps against engineering velocity, and Slack chatter "
            "against strategic priorities to surface what actually matters.</p>"
            "</div>",
            unsafe_allow_html=True,
        )
    with arch_cols[2]:
        st.markdown(
            '<div class="arch-card">'
            "<h4>🔄 Agentic Loop</h4>"
            "<p>Executes a full <strong>Gather → Analyze → Synthesize → Recommend</strong> loop autonomously. "
            "Each run pulls fresh data, identifies risks, and generates prioritized actions "
            "without human prompting.</p>"
            "</div>",
            unsafe_allow_html=True,
        )
    with arch_cols[3]:
        st.markdown(
            '<div class="arch-card">'
            "<h4>⚙️ Production Architecture</h4>"
            "<p><strong>Model-agnostic</strong> LLM provider (swap Gemini ↔ Claude in one line). "
            "Concurrent data fetching via ThreadPoolExecutor. "
            "Structured outputs with source attribution.</p>"
            "</div>",
            unsafe_allow_html=True,
        )

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

# Display brief inside styled container
st.markdown(f'<div class="brief-container">{st.session_state["brief"]}</div>', unsafe_allow_html=True)

if show_raw:
    with st.expander("📋 Raw Data Context (sent to LLM)", expanded=False):
        st.markdown(st.session_state["context"])

# --- Chat history (scrollable, above sticky bar) ---
if "chat_messages" not in st.session_state:
    st.session_state["chat_messages"] = []

if st.session_state["chat_messages"]:
    st.divider()
    for msg in st.session_state["chat_messages"]:
        with st.chat_message(msg["role"], avatar="🧑‍💼" if msg["role"] == "user" else "🦴"):
            st.markdown(msg["content"])

# --- Sticky chat header ---
st.markdown(
    '<div class="sticky-chat-header">'
    '<span style="font-size:1.3rem;">🦴</span>'
    '<span class="label">Ask Your Algae Bud</span>'
    '<span class="sublabel">— answers come strictly from your connected data sources</span>'
    '</div>',
    unsafe_allow_html=True,
)

# Chat input — Streamlit pins this to the bottom automatically
if user_input := st.chat_input("Ask about revenue, products, hiring, customers, Slack updates..."):
    st.session_state["chat_messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="🧑‍💼"):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar="🦴"):
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
