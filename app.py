import streamlit as st
import requests

st.set_page_config(page_title="Chat with your PDF", layout="centered")

st.title("Chat with Your PDF")
st.markdown("Upload a PDF and ask questions based on its content. Powered by LLaMA running locally.")

API_BASE = "http://localhost:8000"

st.subheader("1. Upload a PDF")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    with st.spinner("Uploading and processing the PDF..."):
        files = {"file": uploaded_file.getvalue()}
        response = requests.post(f"{API_BASE}/upload/", files={"file": (uploaded_file.name, uploaded_file, "application/pdf")})
        if response.status_code == 200:
            st.success("PDF uploaded and processed!")
        else:
            st.error("Upload failed. Check if FastAPI server is running.")

st.subheader("2. Ask a Question")
question = st.text_input("Enter your question here:")

if st.button("Ask") and question:
    with st.spinner("Thinking..."):
        response = requests.post(f"{API_BASE}/ask/", data={"question": question})
        if response.status_code == 200:
            answer = response.json().get("answer", "No answer found.")
            st.markdown("**Answer:**")
            st.write(answer)
        else:
            st.error("Error occurred. Try uploading a PDF first.")
