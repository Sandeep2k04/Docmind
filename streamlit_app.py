import requests
import streamlit as st

st.set_page_config(page_title="DocuMind AI", page_icon="📄", layout="wide")
API = st.sidebar.text_input("API URL", "http://localhost:8000").rstrip("/")
st.title("📄 DocuMind AI")
st.caption("Ask questions about your PDFs and inspect the source pages behind each answer.")

with st.sidebar:
    st.header("Upload a document")
    uploaded = st.file_uploader("Choose a PDF", type=["pdf"])
    if uploaded and st.button("Upload PDF", type="primary"):
        try:
            response = requests.post(f"{API}/documents",
                files={"file": (uploaded.name, uploaded.getvalue(), "application/pdf")}, timeout=60)
            response.raise_for_status()
            st.success(f"Uploaded: {response.json()['filename']}")
        except requests.RequestException as exc:
            st.error(f"Upload failed: {exc}")

st.subheader("Your documents")
try:
    response = requests.get(f"{API}/documents", timeout=10)
    response.raise_for_status()
    documents = response.json()
except requests.RequestException:
    documents = []
    st.warning("Could not connect to the API. Start it with: uvicorn app.main:app --reload")

if documents:
    options = {"All documents": None}
    options.update({f"{d['filename']} (ID {d['id']})": d["id"] for d in documents})
    selected = st.selectbox("Search scope", list(options))
    for doc in documents:
        st.write(f"**{doc['filename']}** · {doc['page_count']} pages · ID {doc['id']}")
else:
    selected = "All documents"
    st.info("Upload a text-based PDF to get started.")

st.subheader("Ask your documents")
question = st.text_area("Your question", placeholder="What are the main findings in this report?")
if st.button("Ask", type="primary", disabled=not question.strip()):
    try:
        response = requests.post(f"{API}/ask",
            json={"question": question, "document_id": options[selected] if documents else None},
            timeout=60)
        response.raise_for_status()
        result = response.json()
        st.markdown("### Answer")
        st.write(result["answer"])
        st.caption(f"Answer mode: {result['mode']}")
        st.markdown("### Sources")
        if result["sources"]:
            for source in result["sources"]:
                with st.expander(f"{source['filename']} · page {source['page']}"):
                    st.write(source["excerpt"])
        else:
            st.info("No matching source passages were found.")
    except requests.RequestException as exc:
        st.error(f"Question failed: {exc}")
