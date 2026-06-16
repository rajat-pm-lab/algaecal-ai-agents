"""
CEO Chief of Staff Agent — generates a daily executive brief from live data sources.
Pulls from: Google Sheets (KPIs, products, customers, hiring) + Google Docs (strategy updates).
"""

import os
import sys
from datetime import date

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from shared.llm.provider import call_llm
from shared.connectors.google_sheets import read_sheet
from shared.connectors.google_docs import read_doc

SYSTEM_PROMPT = """You are the AI Chief of Staff for AlgaeCal, a ~100-person DTC health supplements company in Vancouver.
Your job is to produce a concise, actionable daily brief for the CEO.

Rules:
- Lead with the most critical items requiring CEO attention
- Use concrete numbers, not vague language
- Cite the data source for each insight (e.g. "per Google Sheets — Customer Health", "per CEO Weekly Update doc")
- Highlight risks in plain language with dollar impact where possible
- End with 3-5 prioritized recommended actions for today
- Keep the entire brief under 600 words
- Use markdown formatting with headers and bullet points"""


def pull_revenue_kpis() -> str:
    rows = read_sheet("Daily Revenue")
    if not rows:
        return "No revenue data available."

    recent = rows[-7:] if len(rows) >= 7 else rows
    total_rev = sum(float(r.get("Daily Revenue ($)", 0)) for r in recent)
    total_target = sum(float(r.get("Daily Target ($)", 0)) for r in recent)
    variance = ((total_rev - total_target) / total_target) * 100 if total_target else 0

    latest = rows[-1]
    subscribers = latest.get("Active Subscribers", "N/A")
    aov = latest.get("Avg Order Value ($)", "N/A")
    churn = latest.get("Refund Rate (%)", "N/A")
    new_subs = sum(int(r.get("New Subscriptions", 0)) for r in recent)
    churned = sum(int(r.get("Churned Subscriptions", 0)) for r in recent)

    return (
        f"**7-Day Revenue:** ${total_rev:,.0f} vs ${total_target:,.0f} target ({variance:+.1f}%)\n"
        f"**Active Subscribers:** {subscribers} | **AOV:** ${aov} | **Refund Rate:** {churn}%\n"
        f"**7-Day Net Subscriber Change:** +{new_subs} new, -{churned} churned (net +{new_subs - churned})\n"
        f"*Source: Google Sheets — Daily Revenue*"
    )


def pull_product_performance() -> str:
    rows = read_sheet("Product Performance")
    if not rows:
        return "No product data available."

    lines = []
    for r in rows:
        lines.append(
            f"- **{r['Product']}** — ${float(r.get('Revenue ($)', 0)):,.0f} revenue, "
            f"{r.get('Subscription %', 'N/A')}% subscription, "
            f"{r.get('Return Rate (%)', 'N/A')}% return rate, "
            f"Amazon {r.get('Amazon Rating', 'N/A')} stars"
        )
    lines.append("*Source: Google Sheets — Product Performance*")
    return "\n".join(lines)


def pull_customer_health() -> str:
    rows = read_sheet("Customer Health")
    if not rows:
        return "No customer data available."

    at_risk = [r for r in rows if r.get("Risk Level", "").lower() in ("critical", "at risk", "watch")]
    if not at_risk:
        return "All customer accounts healthy.\n*Source: Google Sheets — Customer Health*"

    lines = []
    for r in at_risk:
        lines.append(
            f"- [{r.get('Risk Level', 'Unknown').upper()}] **{r['Account']}** — "
            f"${float(r.get('ARR ($)', 0)):,.0f} ARR, health {r.get('Health Score (0-100)', 'N/A')}/100, "
            f"{r.get('Open Support Tickets', 0)} tickets, renewal {r.get('Renewal Date', 'N/A')}\n"
            f"  {r.get('Notes', '')}"
        )
    lines.append("*Source: Google Sheets — Customer Health*")
    return "\n".join(lines)


def pull_hiring_pipeline() -> str:
    rows = read_sheet("Hiring Pipeline")
    if not rows:
        return "No hiring data available."

    behind = [r for r in rows if r.get("Status", "").lower() in ("behind plan", "at risk")]
    if not behind:
        return "All hiring on track.\n*Source: Google Sheets — Hiring Pipeline*"

    lines = []
    for r in behind:
        lines.append(
            f"- **{r['Role']}** ({r.get('Department', '')}) — "
            f"{r.get('Days Open', '?')} days open, {r.get('Candidates in Pipeline', '?')} candidates, "
            f"top candidate at {r.get('Stage of Top Candidate', 'N/A')}, {r.get('Priority', '')}"
        )
    lines.append("*Source: Google Sheets — Hiring Pipeline*")
    return "\n".join(lines)


def pull_strategy_doc() -> str:
    text = read_doc()
    if not text.strip():
        return "No strategy document content available."
    return f"{text.strip()}\n\n*Source: Google Docs — CEO Weekly Update*"


def build_context() -> str:
    sections = {
        "Revenue & KPIs": pull_revenue_kpis(),
        "Product Performance": pull_product_performance(),
        "Customer Risks": pull_customer_health(),
        "Hiring Pipeline (At Risk)": pull_hiring_pipeline(),
        "CEO Weekly Update (Strategy Doc)": pull_strategy_doc(),
    }

    context = f"**Date:** {date.today().isoformat()}\n\n"
    for title, content in sections.items():
        context += f"### {title}\n{content}\n\n"
    return context


def generate_brief() -> str:
    context = build_context()
    prompt = (
        "Based on the following live company data pulled from Google Sheets and Google Docs, "
        "generate today's CEO Daily Brief.\n\n"
        f"{context}\n\n"
        "Produce the brief now."
    )
    return call_llm(prompt=prompt, system=SYSTEM_PROMPT)
