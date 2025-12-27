import streamlit as st
import requests

st.set_page_config(page_title="Smart Campus Ops", layout="wide")

st.title("🎓 Smart Campus Ops — AI Campus Intelligence")

left, right = st.columns(2)

with left:
    st.subheader("💬 AI Campus Assistant")
    q = st.text_input("Ask a campus question")

    if st.button("Ask"):
        res = requests.post("http://localhost:5000/ask", json={"question": q})
        st.success(res.json()["answer"])

with right:
    st.subheader("📄 Upload Campus Document")
    f = st.file_uploader("Upload PDF", type=["pdf"])

    if f:
        res = requests.post("http://localhost:5000/upload", files={"file": f})
        st.success(res.json()["message"])

    st.divider()

    st.subheader("🚨 Campus Alerts")
    msg = st.text_input("Admin alert")

    if st.button("Send Alert"):
        requests.post("http://localhost:5000/alert", json={"message": msg})
        st.success("Alert sent")

    if st.button("Refresh Alerts"):
        st.write(requests.get("http://localhost:5000/alerts").json())

    st.divider()

    st.subheader("📊 Analytics")
    st.write(requests.get("http://localhost:5000/stats").json())
