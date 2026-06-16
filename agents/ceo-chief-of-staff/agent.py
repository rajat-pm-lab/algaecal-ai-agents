"""
CEO Chief of Staff Agent — generates a daily executive brief from company data.
"""

import sqlite3
import os
import sys
from datetime import date, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from shared.llm.provider import call_llm

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "shared", "data", "algaecal.db")

SYSTEM_PROMPT = """You are the AI Chief of Staff for AlgaeCal, a ~100-person DTC health supplements company in Vancouver.
Your job is to produce a concise, actionable daily brief for the CEO.

Rules:
- Lead with the most critical items
- Use concrete numbers, not vague language
- Highlight risks in plain language
- End with 3-5 prioritized recommended actions for today
- Keep the entire brief under 500 words
- Use markdown formatting with headers and bullet points"""


def get_db():
    return sqlite3.connect(DB_PATH)


def pull_revenue_snapshot():
    conn = get_db()
    c = conn.cursor()
    today = date.today().isoformat()
    week_ago = (date.today() - timedelta(days=7)).isoformat()

    c.execute("SELECT SUM(revenue), SUM(target), AVG(new_customers), AVG(churn_rate), AVG(avg_order_value) FROM kpis WHERE date >= ?", (week_ago,))
    row = c.fetchone()
    conn.close()

    if not row or row[0] is None:
        return "No revenue data available for the past 7 days."

    rev, target, new_cust, churn, aov = row
    variance = ((rev - target) / target) * 100
    return (
        f"**7-Day Revenue:** ${rev:,.0f} vs ${target:,.0f} target ({variance:+.1f}%)\n"
        f"**Avg Daily New Customers:** {new_cust:.0f} | **Churn Rate:** {churn:.1f}% | **AOV:** ${aov:.0f}"
    )


def pull_customer_risks():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT name, arr, health_score, renewal_date, open_tickets, status FROM customers WHERE status IN ('at_risk', 'watch') ORDER BY arr DESC")
    rows = c.fetchall()
    conn.close()

    if not rows:
        return "No customer accounts at risk."

    lines = []
    for name, arr, health, renewal, tickets, status in rows:
        lines.append(f"- **{name}** — ${arr:,.0f} ARR, health score {health}/100, {tickets} open tickets, renewal {renewal}, status: {status}")
    return "\n".join(lines)


def pull_escalations():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT customer, severity, summary, assigned_to, status FROM escalations WHERE status != 'resolved' ORDER BY CASE severity WHEN 'critical' THEN 1 WHEN 'high' THEN 2 ELSE 3 END")
    rows = c.fetchall()
    conn.close()

    if not rows:
        return "No active escalations."

    lines = []
    for cust, sev, summary, assigned, status in rows:
        lines.append(f"- [{sev.upper()}] **{cust}**: {summary} (assigned: {assigned}, {status})")
    return "\n".join(lines)


def pull_initiatives():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT name, owner, status, target_date, progress, blockers, priority FROM initiatives ORDER BY CASE priority WHEN 'P0' THEN 1 WHEN 'P1' THEN 2 ELSE 3 END")
    rows = c.fetchall()
    conn.close()

    lines = []
    for name, owner, status, target, progress, blockers, priority in rows:
        line = f"- [{priority}] **{name}** ({owner}) — {progress}% complete, target {target}, status: {status}"
        if blockers:
            line += f"\n  - Blocker: {blockers}"
        lines.append(line)
    return "\n".join(lines)


def pull_hiring():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT role, department, status, days_open, candidates_in_pipeline FROM hiring WHERE status IN ('behind_plan', 'at_risk') ORDER BY days_open DESC")
    rows = c.fetchall()
    conn.close()

    if not rows:
        return "All hiring on track."

    lines = []
    for role, dept, status, days, candidates in rows:
        lines.append(f"- **{role}** ({dept}) — {days} days open, {candidates} candidates, {status}")
    return "\n".join(lines)


def pull_slack_highlights():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT channel, author, message, importance FROM slack_highlights WHERE importance IN ('critical', 'high') ORDER BY CASE importance WHEN 'critical' THEN 1 ELSE 2 END")
    rows = c.fetchall()
    conn.close()

    if not rows:
        return "No critical Slack highlights."

    lines = []
    for channel, author, msg, imp in rows:
        lines.append(f"- [{imp.upper()}] {channel} ({author}): {msg}")
    return "\n".join(lines)


def build_context():
    sections = {
        "Revenue & KPIs": pull_revenue_snapshot(),
        "Customer Risks": pull_customer_risks(),
        "Active Escalations": pull_escalations(),
        "Engineering Initiatives": pull_initiatives(),
        "Hiring Pipeline (At Risk)": pull_hiring(),
        "Slack Highlights": pull_slack_highlights(),
    }

    context = f"**Date:** {date.today().isoformat()}\n\n"
    for title, content in sections.items():
        context += f"### {title}\n{content}\n\n"
    return context


def generate_brief():
    context = build_context()
    prompt = (
        "Based on the following company data, generate today's CEO Daily Brief.\n\n"
        f"{context}\n\n"
        "Produce the brief now."
    )
    return call_llm(prompt=prompt, system=SYSTEM_PROMPT)


if __name__ == "__main__":
    print(generate_brief())
