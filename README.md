# AlgaeCal AI Agents

A collection of 6 AI agents that act as a digital workforce for [AlgaeCal](https://www.algaecal.com), a ~100-person health supplements company. Each agent replaces hours of manual work with automated intelligence — pulling from CRM, project management, analytics, and communication tools via MCP (Model Context Protocol) integrations.

The goal: demonstrate that a single PM with Claude Code can build production-grade AI agents that deliver measurable business impact.

## Why This Exists

Companies spend millions on operational overhead that AI agents can eliminate:
- Executives waste hours aggregating updates across tools
- PMs manually investigate feature requests and write PRDs
- Customer success teams miss churn signals buried in data
- Revenue teams forecast with gut feel instead of data

These 6 agents solve real problems with real integrations. Not toy demos.

## Agents

| # | Agent | What It Does | Business Impact |
|---|-------|-------------|-----------------|
| 1 | **CEO Chief of Staff** | Daily briefing + "Ask Your Algae Bud" chat: KPIs, risks, hiring, customer escalations | Saves CEO 1-2 hrs/day |
| 2 | **Product Manager Copilot** | Root-cause analysis, PRD generation, experiment design | 3x faster feature investigation |
| 3 | **Customer Success** | Account health scoring, churn prediction, renewal playbooks | Reduces churn |
| 4 | **Revenue Intelligence** | Pipeline analysis, win-loss, deal coaching, forecast | Improves forecast accuracy |
| 5 | **Voice of Customer** | Analyzes support/sales conversations for trends and feature requests | Data-driven product roadmap |
| 6 | **Operations Command Center** | Incident detection, auto-triage, root cause, status updates | Faster MTTR |

## Tech Stack

- **Python 3.11+** — industry standard for AI agents
- **LLM** — model-agnostic (Gemini 2.5 Flash default, Claude API pluggable)
- **MCP** — Model Context Protocol for tool integrations
- **Streamlit** — visual demo UI
- **SQLite** — realistic mock data, zero infrastructure cost

## Quick Start

```bash
git clone https://github.com/rajat-pm-lab/algaecal-ai-agents.git
cd algaecal-ai-agents
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Add your API keys
```

## Project Structure

```
algaecal-ai-agents/
├── agents/
│   ├── ceo-chief-of-staff/     # Agent 1
│   ├── pm-copilot/             # Agent 2
│   ├── customer-success/       # Agent 3
│   ├── revenue-intelligence/   # Agent 4
│   ├── voice-of-customer/      # Agent 5
│   └── ops-command-center/     # Agent 6
├── shared/
│   ├── llm/                    # Model-agnostic LLM provider
│   ├── data/                   # Mock data & SQLite schemas
│   └── mcp/                    # MCP connectors
├── docs/                       # Architecture diagrams
└── requirements.txt
```

## Live Demo

**CEO Chief of Staff Agent** is deployed on Streamlit Cloud with:
- Auto-generated daily brief on page load (parallel data fetching for speed)
- **Ask Your Algae Bud** — conversational AI assistant scoped strictly to company data
- Connected to Google Sheets (KPI Dashboard) + Google Docs (CEO Weekly Update)

## Architecture

Each agent follows the same pattern:
1. **Data layer** — MCP connectors pull from business tools (Jira, Salesforce, Slack, etc.)
2. **Intelligence layer** — LLM analyzes, synthesizes, and reasons over the data
3. **Output layer** — Structured recommendations delivered via Streamlit UI or CLI

The LLM provider is swappable — change `LLM_PROVIDER=gemini` to `LLM_PROVIDER=anthropic` in `.env` to switch models.

## Author

**Rajat Singh** — Senior Product Manager | AI Product Builder

Building this portfolio to demonstrate that modern PMs should be able to architect and ship AI agents, not just write PRDs about them.

[GitHub](https://github.com/rajat-pm-lab)
