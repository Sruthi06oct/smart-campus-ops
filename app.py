import streamlit as st
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from PyPDF2 import PdfReader

st.set_page_config(page_title="Smart Campus Ops", layout="wide")

@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_model()

if "texts" not in st.session_state:
    st.session_state.texts = []
if "index" not in st.session_state:
    st.session_state.index = None
if "alerts" not in st.session_state:
    st.session_state.alerts = []
if "queries" not in st.session_state:
    st.session_state.queries = []

def load_pdf(file):
    texts = []
    reader = PdfReader(file)
    for p in reader.pages:
        t = p.extract_text()
        if t:
            texts.extend(t.split("\n"))
    emb = model.encode(texts)
    index = faiss.IndexFlatL2(emb.shape[1])
    index.add(np.array(emb))
    st.session_state.texts = texts
    st.session_state.index = index

def retrieve(q, k=3):
    if st.session_state.index is None:
        return ["Upload a document first."]
    q_emb = model.encode([q])
    D, I = st.session_state.index.search(np.array(q_emb), k)
    return [st.session_state.texts[i] for i in I[0]]

left, right = st.columns(2)

with left:
    st.header("💬 AI Campus Assistant")
    q = st.text_input("Ask a campus question")
    if st.button("Ask"):
        st.session_state.queries.append(q)
        st.success("\n".join(retrieve(q)))

with right:
    st.header("📄 Upload Campus PDF")
    f = st.file_uploader("Upload PDF", type=["pdf"])
    if f:
        load_pdf(f)
        st.success("PDF processed")

    st.divider()
    st.header("🚨 Campus Alerts")
    msg = st.text_input("Admin alert")
    if st.button("Send Alert"):
        st.session_state.alerts.append(msg)
    st.write(st.session_state.alerts)

    st.divider()
    st.header("📊 Analytics")
    st.write({"total_queries": len(st.session_state.queries)})

