"""
Seeds SQLite DB with realistic AlgaeCal mock data for all agents.
Run: python -m shared.data.seed
"""

import sqlite3
import os
from datetime import date, timedelta
import random

DB_PATH = os.path.join(os.path.dirname(__file__), "algaecal.db")


def get_db():
    return sqlite3.connect(DB_PATH)


def seed():
    conn = get_db()
    c = conn.cursor()

    # --- Revenue / KPIs ---
    c.execute("DROP TABLE IF EXISTS kpis")
    c.execute("""
        CREATE TABLE kpis (
            date TEXT, revenue REAL, target REAL, new_customers INTEGER,
            churn_rate REAL, avg_order_value REAL, ltv REAL
        )
    """)
    today = date.today()
    for i in range(30):
        d = today - timedelta(days=29 - i)
        target = 45000 + random.randint(-2000, 2000)
        revenue = target + random.randint(-8000, 6000)
        c.execute("INSERT INTO kpis VALUES (?,?,?,?,?,?,?)", (
            d.isoformat(), revenue, target,
            random.randint(20, 60),
            round(random.uniform(1.5, 4.0), 2),
            round(random.uniform(55, 85), 2),
            round(random.uniform(280, 420), 2),
        ))

    # --- Enterprise Customers ---
    c.execute("DROP TABLE IF EXISTS customers")
    c.execute("""
        CREATE TABLE customers (
            id INTEGER PRIMARY KEY, name TEXT, segment TEXT,
            arr REAL, health_score INTEGER, renewal_date TEXT,
            last_nps INTEGER, open_tickets INTEGER, status TEXT
        )
    """)
    customers = [
        ("Whole Foods Partnership", "enterprise", 320000, 85, "2026-08-15", 9, 1, "healthy"),
        ("Costco Canada", "enterprise", 580000, 42, "2026-07-01", 5, 7, "at_risk"),
        ("Amazon Marketplace", "enterprise", 450000, 38, "2026-09-30", 4, 12, "at_risk"),
        ("Vitacost Distribution", "enterprise", 210000, 30, "2026-07-15", 3, 5, "at_risk"),
        ("GNC Retail Program", "enterprise", 175000, 72, "2026-10-01", 8, 2, "healthy"),
        ("iHerb Channel", "enterprise", 290000, 68, "2026-11-15", 7, 3, "healthy"),
        ("Shoppers Drug Mart", "enterprise", 155000, 55, "2026-08-01", 6, 4, "watch"),
        ("Natural Grocers", "strategic", 95000, 78, "2027-01-15", 8, 0, "healthy"),
        ("Thrive Market", "strategic", 120000, 61, "2026-12-01", 7, 2, "healthy"),
        ("Well.ca", "mid-market", 45000, 82, "2027-03-01", 9, 0, "healthy"),
    ]
    for cust in customers:
        c.execute("INSERT INTO customers (name,segment,arr,health_score,renewal_date,last_nps,open_tickets,status) VALUES (?,?,?,?,?,?,?,?)", cust)

    # --- Engineering Initiatives ---
    c.execute("DROP TABLE IF EXISTS initiatives")
    c.execute("""
        CREATE TABLE initiatives (
            id INTEGER PRIMARY KEY, name TEXT, owner TEXT,
            status TEXT, target_date TEXT, progress INTEGER,
            blockers TEXT, priority TEXT
        )
    """)
    initiatives = [
        ("Subscription Platform v2", "Sarah Chen", "delayed", "2026-06-30", 62, "Payment provider API migration blocked on legal review", "P0"),
        ("Mobile App Rewrite (React Native)", "Marcus Johnson", "delayed", "2026-07-15", 45, "iOS push notifications failing in TestFlight", "P0"),
        ("AI-Powered Product Recommendations", "Priya Patel", "on_track", "2026-08-01", 35, None, "P1"),
        ("Customer Portal Redesign", "David Kim", "on_track", "2026-07-30", 70, None, "P1"),
        ("Warehouse Automation Phase 2", "Lisa Wang", "at_risk", "2026-06-25", 80, "Vendor delivery of conveyor system delayed 2 weeks", "P0"),
        ("International Shipping Expansion", "James Taylor", "on_track", "2026-09-15", 20, None, "P2"),
    ]
    for init in initiatives:
        c.execute("INSERT INTO initiatives (name,owner,status,target_date,progress,blockers,priority) VALUES (?,?,?,?,?,?,?)", init)

    # --- Hiring Pipeline ---
    c.execute("DROP TABLE IF EXISTS hiring")
    c.execute("""
        CREATE TABLE hiring (
            id INTEGER PRIMARY KEY, role TEXT, department TEXT,
            status TEXT, days_open INTEGER, candidates_in_pipeline INTEGER,
            hiring_manager TEXT
        )
    """)
    hiring = [
        ("Senior Backend Engineer", "Engineering", "behind_plan", 45, 2, "Sarah Chen"),
        ("Senior Backend Engineer", "Engineering", "behind_plan", 38, 1, "Sarah Chen"),
        ("ML Engineer", "Data Science", "behind_plan", 52, 3, "Priya Patel"),
        ("Product Designer", "Design", "on_track", 20, 5, "David Kim"),
        ("Customer Success Manager", "CS", "on_track", 15, 4, "Rachel Green"),
        ("Marketing Analyst", "Marketing", "on_track", 10, 6, "Tom Wilson"),
        ("DevOps Engineer", "Engineering", "at_risk", 35, 2, "Marcus Johnson"),
    ]
    for h in hiring:
        c.execute("INSERT INTO hiring (role,department,status,days_open,candidates_in_pipeline,hiring_manager) VALUES (?,?,?,?,?,?)", h)

    # --- Customer Escalations ---
    c.execute("DROP TABLE IF EXISTS escalations")
    c.execute("""
        CREATE TABLE escalations (
            id INTEGER PRIMARY KEY, customer TEXT, severity TEXT,
            summary TEXT, created_date TEXT, assigned_to TEXT, status TEXT
        )
    """)
    escalations = [
        ("Costco Canada", "critical", "Shipment of 10,000 units delayed — Costco threatening contract review", (today - timedelta(days=2)).isoformat(), "VP Operations", "open"),
        ("Amazon Marketplace", "critical", "Product listing suspended due to labeling compliance issue", (today - timedelta(days=1)).isoformat(), "VP Regulatory", "open"),
        ("Vitacost Distribution", "high", "Billing dispute — $45K invoice discrepancy from Q1", (today - timedelta(days=5)).isoformat(), "CFO", "in_progress"),
        ("Shoppers Drug Mart", "medium", "Requesting exclusive Canadian formulation — needs CEO decision", (today - timedelta(days=3)).isoformat(), "VP Product", "open"),
    ]
    for esc in escalations:
        c.execute("INSERT INTO escalations (customer,severity,summary,created_date,assigned_to,status) VALUES (?,?,?,?,?,?)", esc)

    # --- Recent Slack Highlights (simulated) ---
    c.execute("DROP TABLE IF EXISTS slack_highlights")
    c.execute("""
        CREATE TABLE slack_highlights (
            id INTEGER PRIMARY KEY, channel TEXT, author TEXT,
            message TEXT, timestamp TEXT, importance TEXT
        )
    """)
    highlights = [
        ("#revenue", "Tom Wilson", "June DTC revenue tracking 8% above forecast — subscription upgrades driving growth", (today - timedelta(hours=6)).isoformat(), "high"),
        ("#engineering", "Sarah Chen", "Payment provider migration: legal review expected to close by Wednesday", (today - timedelta(hours=4)).isoformat(), "high"),
        ("#cx-escalations", "Rachel Green", "Costco account manager requesting emergency call with our CEO by EOD Tuesday", (today - timedelta(hours=3)).isoformat(), "critical"),
        ("#product", "David Kim", "Customer portal beta NPS: 72 — strong positive signal from test group", (today - timedelta(hours=8)).isoformat(), "medium"),
        ("#hiring", "HR Team", "Backend engineer pipeline critically low — recommending recruiter agency engagement", (today - timedelta(hours=5)).isoformat(), "high"),
        ("#operations", "Lisa Wang", "Warehouse conveyor vendor confirmed revised delivery: June 28", (today - timedelta(hours=2)).isoformat(), "medium"),
    ]
    for h in highlights:
        c.execute("INSERT INTO slack_highlights (channel,author,message,timestamp,importance) VALUES (?,?,?,?,?)", h)

    conn.commit()
    conn.close()
    print(f"Seeded {DB_PATH}")


if __name__ == "__main__":
    seed()
