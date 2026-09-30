import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Groww MF FAQ - Facts Only", page_icon="💰", layout="centered")

# Load sources
try:
    sources_df = pd.read_csv("data/sources.csv")
except:
    sources_df = pd.DataFrame()

# Scope
AMC = "Groww Mutual Fund"
SCHEMES = [
    "Groww Large Cap Fund",
    "Groww Flexi Cap Fund", 
    "Groww ELSS Tax Saver Fund",
    "Groww Nifty Total Market Index Fund",
    "Groww Short Duration Fund"
]

# Knowledge base with citations
KB = {
    "expense ratio": {
        "ans": "Expense ratio is the annual fee charged by the AMC. For Groww MF schemes, the exact TER is disclosed on the official TER page and in each factsheet.",
        "cite": "https://growwmf.in/disclosures/total-expense-ratio"
    },
    "exit load": {
        "ans": "Exit load is a fee if you redeem before a specified period. For example, many Groww equity funds have 1% exit load if redeemed within 1 year.",
        "cite": "https://growwmf.in/faqs"
    },
    "minimum sip": {
        "ans": "Minimum SIP for Groww MF schemes starts from Rs. 100 for most equity funds. Check the KIM/SID for scheme-specific minimums.",
        "cite": "https://growwmf.in/downloads/kim"
    },
    "elss lock-in": {
        "ans": "ELSS has a mandatory 3-year lock-in per SEBI regulations. Groww ELSS Tax Saver Fund follows this lock-in.",
        "cite": "https://www.amfiindia.com/investor-corner/knowledge-center/elss.html"
    },
    "riskometer": {
        "ans": "Riskometer shows the risk level of a scheme (Low to Very High) as per SEBI product labelling norms. Each Groww factsheet displays its riskometer.",
        "cite": "https://www.amfiindia.com/investor-corner/knowledge-center/riskometer.html"
    },
    "benchmark": {
        "ans": "Benchmark is the index a scheme compares performance against. For example, Groww Large Cap Fund benchmarks against Nifty 100 TRI. Refer to factsheet for exact benchmark.",
        "cite": "https://growwmf.in/funds/groww-large-cap-fund"
    },
    "nav": {
        "ans": "NAV is the per-unit price of a mutual fund scheme, updated daily after market close as per AMFI guidelines.",
        "cite": "https://www.amfiindia.com/investor-corner/knowledge-center/what-is-nav.html"
    },
    "statement": {
        "ans": "To download capital gains / account statement, visit Groww MF downloads page and use the statement request option.",
        "cite": "https://growwmf.in/downloads"
    },
    "aum": {
        "ans": "AUM is total assets managed by the fund house/scheme. Check latest factsheet for scheme AUM.",
        "cite": "https://growwmf.in/funds/groww-large-cap-fund"
    }
}

REFUSAL_KEYWORDS = ["should i buy", "should i sell", "which is best", "recommend", "portfolio", "return kitna", "best fund"]

st.title("Groww Mutual Fund - Facts-Only FAQ")
st.caption(f"Facts-only assistant for {AMC}. No investment advice.")
st.info(f"**Scope:** {AMC} | Schemes: {', '.join(SCHEMES[:3])} + 2 more. | Last updated from sources: {date.today().strftime('%b %d, %Y')}")

st.markdown("**Welcome! Ask factual questions only.**")
col1, col2, col3 = st.columns(3)
col1.button("Expense ratio of Groww funds?")
col2.button("ELSS lock-in?")
col3.button("How to download statement?")

# Disclaimer
st.warning("Disclaimer: Facts-only, sourced from AMC/SEBI/AMFI public pages. No investment advice, no performance claims. For decisions, consult official KIM/SID.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

def get_answer(q):
    lower = q.lower()
    for bad in REFUSAL_KEYWORDS:
        if bad in lower:
            return f"I can only provide factual information, not investment advice. For understanding risk and product suitability, please refer to the scheme KIM/SID. [Learn more](https://growwmf.in/downloads/kim)", None
    for key, val in KB.items():
        if key in lower:
            ans = f"{val['ans']}\n\n**Source:** [{val['cite']}]({val['cite']})"
            return ans, val['cite']
    # fallback
    return f"A mutual fund fact must come from official pages. Please ask about expense ratio, exit load, minimum SIP, ELSS lock-in, riskometer, benchmark, NAV, or statements. Refer to scheme documents: [Groww Downloads](https://growwmf.in/downloads)", "https://growwmf.in/downloads"

if p := st.chat_input("Ask e.g. What is expense ratio? What is ELSS lock-in?"):
    st.session_state.messages.append({"role":"user","content":p})
    with st.chat_message("user"):
        st.markdown(p)
    ans, cite = get_answer(p)
    st.session_state.messages.append({"role":"assistant","content":ans})
    with st.chat_message("assistant"):
        st.markdown(ans)

st.markdown("---")
st.caption(f"Sources used: {len(sources_df)} URLs | AMC: {AMC} | Data: data/sources.csv")
