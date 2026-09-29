import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
st.set_page_config(page_title="Groww MF - FAQ Assistant", page_icon="💹", layout="wide")
FAQ_DATA = [
    {"q": "What is ELSS and tax benefit?", "a": "ELSS offers tax deduction up to Rs 1.5 lakh under Section 80C. Groww ELSS Tax Saver Fund has 3-year lock-in.", "source": "https://www.growwmf.in/mutual-funds/groww-elss-tax-saver-fund-direct-growth"},
    {"q": "How to download CAS statement?", "a": "Download CAS from CAMS or KFintech. Visit camsonline.com or kfintech.com.", "source": "https://www.camsonline.com/Investors/Statements"},
    {"q": "What is Riskometer?", "a": "Riskometer shows risk level - Low to Very High. Mandated by SEBI.", "source": "https://www.growwmf.in/downloads/riskometer"},
    {"q": "What is expense ratio?", "a": "Annual fee charged by AMC. Groww direct plans ~0.3-0.6% for equity.", "source": "https://www.growwmf.in/downloads/sai"},
    {"q": "What is cut-off time?", "a": "Equity funds 3 PM same day NAV, after 3 PM next day NAV. Liquid 1:30 PM.", "source": "https://www.growwmf.in/downloads/kim"},
]
@st.cache_resource
def get_vectorizer():
    v = TfidfVectorizer()
    vecs = v.fit_transform([x['q'] for x in FAQ_DATA])
    return v, vecs
vectorizer, q_vectors = get_vectorizer()
st.title("Groww Mutual Fund - FAQ Assistant")
st.caption("RAG based FAQ search - English Version")
query = st.text_input("Ask your question (e.g. What is ELSS?)", "")
if query:
    q_vec = vectorizer.transform([query])
    sims = cosine_similarity(q_vec, q_vectors)[0]
    top_idx = sims.argsort()[-3:][::-1]
    for idx in top_idx:
        if sims[idx] > 0.1:
            item = FAQ_DATA[idx]
            with st.container(border=True):
                st.markdown(f"**Q: {item['q']}** (Score: {sims[idx]:.2f})")
                st.write(item['a'])
                st.link_button("View Source", item['source'])
