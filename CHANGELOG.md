# Changelog

All notable changes to this project are documented here.

## [0.3.0] — 2026-06-16

### Added
- **Ask Your Algae Bud** — conversational chat interface below the daily brief
  - Multi-turn Q&A grounded strictly in connected data sources (Google Sheets + Docs)
  - CEO can ask follow-up questions about revenue, products, hiring, customers
  - Refuses to answer from outside knowledge — scoped to company data only
- **Auto-generate brief on page load** — CEO sees the brief immediately without clicking a button
- **Parallel data fetching** — all 5 data sources pulled simultaneously via ThreadPoolExecutor (~3x faster)
- **Refresh Brief** button in sidebar for manual re-pull

### Changed
- `agent.py` — `build_context()` now uses concurrent.futures for parallel API calls
- `agent.py` — `generate_brief()` accepts pre-built context to avoid double-fetching
- `streamlit_app.py` / `app.py` — complete UI rewrite with auto-load + chat

### Performance
- Brief generation reduced from ~7-10s to ~2-4s (parallel fetching eliminates serial API bottleneck)

## [0.2.0] — 2026-06-15

### Added
- Streamlit Cloud deployment support
- Google Sheets connector (reads KPI Dashboard: Daily Revenue, Product Performance, Customer Health, Hiring Pipeline)
- Google Docs connector (reads CEO Weekly Update strategy doc)
- Root `streamlit_app.py` entry point for Streamlit Cloud auto-detection
- Live data sources sidebar with connection status indicators

### Fixed
- Removed `__main__` block from agent.py to prevent Streamlit Cloud crash
- Added missing dependencies and error handling for Streamlit Cloud blank page

## [0.1.0] — 2026-06-14

### Added
- Initial project scaffold: monorepo structure for 6 AI agents
- Model-agnostic LLM provider (`shared/llm/provider.py`) — supports Gemini 2.5 Flash + Anthropic Claude
- CEO Chief of Staff Agent with mock data and Streamlit UI
- System prompt for executive daily brief generation
- Config helper with .env + Streamlit secrets fallback
