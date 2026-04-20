
# Local Agentic RAG System (HuggingFace + FAISS)

This project implements a **local Deep Research / Agentic RAG system**.

Features:
- Local LLM (HuggingFace Transformers)
- Embeddings using Sentence Transformers
- Vector search (FAISS)
- Keyword search (BM25)
- Tool-based agent
- Document ingestion pipeline

## Install

pip install -r requirements.txt

## Add Documents

Put PDFs or text files into:

data/documents/

## Run

python g.py
streamlit run app.py

