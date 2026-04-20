import streamlit as st
from pathlib import Path

from src.document_loader import load_documents
from src.chunking import chunk_text
from src.vector_index import VectorIndex
from src.bm25_index import BM25Index
from src.tools import Tools
from src.agent import DeepResearchAgent


# -----------------------------
# Page Config
# -----------------------------

st.set_page_config(
    page_title="Agentic RAG",
    layout="wide",
    initial_sidebar_state="collapsed"
)

DATA_DIR = Path("data/pdfs")
DATA_DIR.mkdir(parents=True, exist_ok=True)


# -----------------------------
# Header
# -----------------------------

st.title("📚 Agentic RAG System")
st.caption("Intelligent Document Analysis Powered by Deep Research")


# -----------------------------
# Sidebar Upload
# -----------------------------

with st.sidebar:
    st.header("📂 Upload Documents")

    uploaded_files = st.file_uploader(
        "Upload PDF files",
        type=["pdf"],
        accept_multiple_files=True
    )

    if uploaded_files:
        for file in uploaded_files:
            save_path = DATA_DIR / file.name
            with open(save_path, "wb") as f:
                f.write(file.read())

        st.success("Documents uploaded successfully!")
        st.rerun()


# -----------------------------
# Initialize RAG system
# -----------------------------

@st.cache_resource
def initialize_system():

    docs = load_documents()

    if not docs:
        return None

    chunks = []
    for d in docs:
        chunks.extend(chunk_text(d))

    vector = VectorIndex()
    vector.build(chunks)

    bm25 = BM25Index()
    bm25.build(chunks)

    tools = Tools(vector, bm25)

    agent = DeepResearchAgent(tools)

    return agent


agent = initialize_system()


# -----------------------------
# Question input
# -----------------------------

question = st.text_input(
    "Ask a question about your documents",
    placeholder="Example: What is the return policy?"
)


# -----------------------------
# Answer section
# -----------------------------

if question:

    if agent is None:
        st.warning("⚠️ Please upload at least one document first.")
    else:

        with st.spinner("Analyzing documents..."):
            answer = agent.run(question)

        st.markdown("### 🤖 Answer")
        st.write(answer)