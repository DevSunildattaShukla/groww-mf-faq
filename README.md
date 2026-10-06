# Groww Mutual Fund FAQ Assistant - Milestone 5

## Milestone 5 Deliverables (All English)

### 1. Review Intelligence Layer
- File: `data/reviews_last_10_weeks.csv` (30 reviews)
- Analysis: 5 themes max, top 3 with counts
- Recurring Fee Confusion: Exit Load (1% if <30 days for equity, graded 7 days for liquid) and Stamp Duty 0.005% mistaken as Groww fee

### 2. Internal Product Pulse
- File: `internal_notes/product_pulse_log.md` (Cumulative log)
- Weekly format: Date, Summary, 3 Supporting Quotes, Key Observation, 3 Action Ideas
- Under 150 words, internal use only, dated

### 3. Fee Explainer (Source-verified)
- Inline in app.py and README: 5-8 bullets
- Includes: AMC charges exit load not Groww, equity 30 days, liquid 7 days, stamp duty 0.005% govt levy since July 1 2020 per SEBI circular, deducted from units/proceeds, refer SID/KIM
- Sources: 
    - https://groww.in/mutual-funds/faq/exit-load
    - https://www.sebi.gov.in/legal/circulars/jun-2020/stamp-duty-on-mutual-fund-transactions_46880.html
- Last checked: 2026-10-06

### 4. MCP Actions (Approval-Gated)
- Action 1: Append to Doc -> `internal_notes/product_pulse_log.md` + JSON log `internal_notes/log_{date}.json`
- Action 2: Create Email Draft -> `email_drafts/draft_{date}.eml` (No auto-send)
- Approval: Checkbox "I approve logging..." + Confirm button
- Evidence: Logged content includes themes, pulse, fee issue, explanation bullets, source links

### 5. Workflow Flow
Reviews CSV -> Theme Clustering (max 5) -> Weekly Pulse (<150w, 3 quotes, 3 ideas) -> Fee Explainer (5-8 bullets + 2 sources) -> MCP Logging (Doc + Email Draft) with human approval

## Run
streamlit run app.py
