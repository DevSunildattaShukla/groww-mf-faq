import streamlit as st
from datetime import date
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Groww MF FAQ", page_icon="💰")
st.title("Groww Mutual Fund - Facts-Only FAQ Assistant")
st.markdown("**Facts-only. No investment advice.**")
st.info("Welcome! Ask about expense ratio, exit load, minimum SIP, ELSS lock-in, riskometer, benchmark, or statement download.")

KB = [
    {"text": "Groww ELSS Tax Saver Fund has a statutory lock-in period of 3 years as per ELSS rules.", "url": "https://www.growwmf.in/downloads/kim"},
    {"text": "Minimum SIP for Groww Large Cap Fund Direct Growth is Rs 500.", "url": "https://www.growwmf.in/mutual-funds/groww-large-cap-fund-direct-growth"},
    {"text": "Expense ratio details are disclosed in factsheet and expense ratio page.", "url": "https://www.growwmf.in/downloads/expense-ratio"},
    {"text": "Exit load is charged if redeemed within specified period. Refer SID for scheme-wise exit load.", "url": "https://www.growwmf.in/downloads/sid"},
    {"text": "Riskometer indicates risk level of scheme. Refer riskometer disclosure page.", "url": "https://www.growwmf.in/downloads/riskometer"},
    {"text": "Benchmark for Groww Large Cap Fund is Nifty 100 TRI. Check factsheet.", "url": "https://www.growwmf.in/downloads/fact-sheet"},
    {"text": "To download capital gains statement, visit CAMS or KFintech or AMFI CAS download page.", "url": "https://www.amfiindia.com/online-center/download-cas"},
]

def has_pii(q): return bool(re.search(r'\b\d{10}\b|[A-Z]{5}\d{4}[A-Z]|otp', q, re.I))
def is_advice(q): return any(k in q.lower() for k in ["should i buy", "should i sell", "recommend", "best fund"])
def is_perf(q): return any(k in q.lower() for k in ["return", "performance", "compare", "cagr"])

query = st.text_input("Your question:")
if query:
    if has_pii(query):
        st.error("Please don't share PAN, Aadhaar, phone, OTP")
    elif is_advice(query):
        st.warning("I can only share facts. Learn: https://www.amfiindia.com/investor-knowledge-center")
    elif is_perf(query):
        st.warning("I don't calculate returns. See: https://www.growwmf.in/downloads/fact-sheet")
    else:
        texts = [k["text"] for k in KB]
        vectorizer = TfidfVectorizer().fit(texts + [query])
        vecs = vectorizer.transform(texts + [query])
        sim = cosine_similarity(vecs[-1], vecs[:-1]).flatten()
        best = KB[sim.argmax()]
        st.success(f"{best['text']}\n\nSource: {best['url']}\n\nLast updated: {date.today()}")
