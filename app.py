import streamlit as st

st.set_page_config(page_title="Groww MF FAQ - Facts Only", page_icon="💰", layout="centered")

st.title("Groww Mutual Fund - Facts-Only FAQ")
st.caption("Facts-only assistant. No investment advice.")

faqs = {
    "what is mutual fund": "A mutual fund pools money from many investors and invests in stocks, bonds etc. Managed by an AMC.",
    "what is sip": "SIP is Systematic Investment Plan - you invest a fixed amount regularly (monthly). On Groww you can start from Rs 100.",
    "what is nav": "NAV is Net Asset Value - price of one unit of a mutual fund. Updated daily after market close.",
    "what is expense ratio": "Expense ratio is the annual fee charged by AMC for managing the fund. Lower expense ratio means more of your money stays invested.",
    "what is elss": "ELSS is Equity Linked Savings Scheme - tax saving MF with 3-year lock-in. Deduction up to 1.5L under 80C.",
    "what is aum": "AUM is Assets Under Management - total value of assets managed by the fund house.",
    "direct vs regular": "Direct plan has lower expense ratio as you invest directly. Regular plan is via distributor with higher expense ratio."
}

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if p := st.chat_input("Ask e.g. What is SIP? What is NAV?"):
    st.session_state.messages.append({"role":"user","content":p})
    with st.chat_message("user"):
        st.markdown(p)
    
    lower = p.lower()
    ans = "I can answer only facts: Try - What is mutual fund, What is SIP, What is NAV, What is expense ratio, What is ELSS, Direct vs Regular"
    for k,v in faqs.items():
        if k in lower:
            ans = v
            break
    
    st.session_state.messages.append({"role":"assistant","content":ans})
    with st.chat_message("assistant"):
        st.markdown(ans)

st.divider()
st.markdown("**Sample questions:** What is SIP? | What is NAV? | What is ELSS? | Direct vs Regular")
