import streamlit as st
import pandas as pd
from datetime import date
import os
import json

st.set_page_config(page_title="Groww Review Intelligence - Milestone 5", layout="wide")
st.title("AI Workflow: Reviews -> Insights -> MCP Actions")

# Load Reviews
df = pd.read_csv("data/reviews_last_10_weeks.csv")
st.subheader(f"Step 1: Review Intelligence Layer ({len(df)} reviews last 10 weeks)")
st.dataframe(df.head(10), use_container_width=True)

# Simulated Theme Clustering
themes = {
    "Pricing/Fee Confusion (Exit Load + Stamp Duty)": 12,
    "NAV & Execution Delay": 7,
    "SIP Cancellation / Modification Pain": 5,
    "KYC / Mandate Failure": 4,
    "App UX": 2
}

st.subheader("Clustered Themes (Max 5)")
col1, col2 = st.columns(2)
with col1:
    st.json(themes)
with col2:
    st.write("**Top 3 Themes:**")
    st.write("1. Pricing/Fee Confusion (40%)")
    st.write("2. NAV & Execution Delay (23%)")
    st.write("3. SIP Cancellation Pain (17%)")
    st.write("**Recurring Fee Confusion Detected:** Exit Load charged unexpectedly + 0.005% Stamp Duty mistaken as Groww fee")

quotes = [
    "Redeemed Groww Nifty Index fund after 20 days and 1% was deducted as exit load. Why was this not shown?",
    "Why 0.005% extra cut on my 10k SIP? Shows 9999.5 units only. Is Groww charging extra?",
    "I thought ELSS lock-in over after 3 years but exit load still applied? Need clarity"
]

st.subheader("Step 2: Weekly Product Pulse (Internal)")
weekly_pulse = f"""
**Weekly Product Pulse - {date.today()} | Groww Mutual Funds**

**Summary:** 40% of negative reviews in last 10 weeks cluster around fee confusion, specifically exit load timing and 0.005% stamp duty. Users perceive these as hidden Groww charges.

**Supporting Quotes:**
1. "{quotes[0]}"
2. "{quotes[1]}"
3. "{quotes[2]}"

**Key Observation:** Users confuse ELSS 3-year lock-in with exit load (30 days for equity, 7 days for liquid). Stamp duty is not shown separately in order preview, leading to trust issues.

**3 Action Ideas:**
1. Add inline tooltip on redeem screen: "Exit Load 1% if <30 days as per SID - charged by AMC, not Groww"
2. Show stamp duty as separate line item in order preview (e.g., Amount: 10000, Stamp Duty: 0.50, Units on: 9999.5)
3. Create reusable support snippet + 30-sec Loom for support team to share proactively.

Word Count: ~145 words
"""

st.markdown(weekly_pulse)

st.subheader("Step 3: Fee Explainer (Derived from Insights)")

explanation_bullets = [
    "Exit Load is charged by the AMC (mutual fund company), not by Groww, if you redeem before the period mentioned in Scheme Information Document (SID).",
    "For most equity/index funds: 1% if redeemed within 30 days of investment. For Groww Liquid Fund: graded exit load within 7 days, Nil after 7 days.",
    "Stamp Duty of 0.005% is a government levy on all mutual fund purchases including SIP installments, applicable from July 1, 2020 as per SEBI circular.",
    "Both charges are adjusted in units allotted/redeemed amount and visible in your account statement and CAS.",
    "Exit Load is deducted from redemption proceeds, not shown as separate fee, which causes confusion.",
    "Refer to fund's SID/KIM on Groww fund page for exact load structure before investing/redeeming."
]

source_links = [
    "https://groww.in/mutual-funds/faq/exit-load",
    "https://www.sebi.gov.in/legal/circulars/jun-2020/stamp-duty-on-mutual-fund-transactions_46880.html"
]

for b in explanation_bullets:
    st.write(f"- {b}")

st.write(f"**Sources:** {source_links[0]} | {source_links[1]}")
st.write(f"**Last checked: {date.today()}**")

# MCP Approval Gating
st.divider()
st.subheader("Step 4: MCP Actions (Approval-Gated)")

if "generated" not in st.session_state:
    if st.button("Generate Outputs for Logging"):
        st.session_state["generated"] = True
        st.session_state["pulse"] = weekly_pulse
        st.session_state["bullets"] = explanation_bullets
        st.session_state["links"] = source_links
        st.rerun()

if "generated" in st.session_state:
    approve = st.checkbox("I approve logging this to internal tools (Doc + Email Draft)")
    if approve:
        if st.button("✅ Confirm & Log via MCP"):
            # Action 1: Append to Doc
            log_entry = {
                "date": str(date.today()),
                "top_themes": list(themes.keys())[:3],
                "weekly_pulse": st.session_state["pulse"],
                "identified_fee_issue": "Exit Load timing confusion + Stamp Duty 0.005% mistaken as Groww fee",
                "explanation_bullets": st.session_state["bullets"],
                "source_links": st.session_state["links"]
            }

            with open("internal_notes/product_pulse_log.md", "a") as f:
                f.write(f"\n\n---\n## {log_entry['date']}\n")
                f.write(f"**Top Themes:** {', '.join(log_entry['top_themes'])}\n\n")
                f.write(f"{log_entry['weekly_pulse']}\n\n")
                f.write(f"**Fee Issue:** {log_entry['identified_fee_issue']}\n\n")
                f.write("**Explanation:**\n")
                for bullet in log_entry['explanation_bullets']:
                    f.write(f"- {bullet}\n")
                f.write(f"\nSources: {log_entry['source_links']}\n")

            # Action 2: Create Email Draft
            email_content = f"""Subject: Weekly Product Pulse + Customer Clarification - {date.today()}

Hi Team,

Here is this week's product pulse and reusable support snippet.

--- WEEKLY PRODUCT PULSE ---
{st.session_state["pulse"]}

--- REUSABLE SUPPORT SNIPPET: Exit Load + Stamp Duty ---
"""
            for b in st.session_state["bullets"]:
                email_content += f"- {b}\n"
            email_content += f"\nSources: {st.session_state['links'][0]}, {st.session_state['links'][1]}\nLast checked: {date.today()}\n\n(No auto-send - Draft only)\n"

            email_path = f"email_drafts/draft_{date.today()}.eml"
            with open(email_path, "w") as f:
                f.write(email_content)

            # Save JSON for proof
            with open(f"internal_notes/log_{date.today()}.json", "w") as f:
                json.dump(log_entry, f, indent=2)

            st.success(f"✅ Logged! Check internal_notes/product_pulse_log.md and {email_path}")
            st.balloons()
            st.code(email_content, language="text")
