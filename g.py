import gradio as gr
import os
from src.agent import DeepResearchAgent
from src.document_loader import load_documents
from src.chunking import chunk_text
from src.vector_index import VectorIndex
from src.bm25_index import BM25Index
from src.tools import Tools

# 1. Setup Data Directory
DATA_DIR = "data/pdfs"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# 2. System Initialization (Runs once when you start the script)
def initialize_system():
    print("🔄 Re-scanning data/pdfs...")
    docs = load_documents() # Uses your NEW PyMuPDF loader
    
    if not docs:
        print("❌ No documents found!")
        return None

    # Force a fresh chunking of the NEW documents
    all_chunks = []
    for d in docs:
        all_chunks.extend(chunk_text(d))
    
    print(f"📦 Created {len(all_chunks)} chunks.")

    # Rebuild indexes from scratch
    vector = VectorIndex()
    vector.build(all_chunks)

    bm25 = BM25Index()
    bm25.build(all_chunks)

    return DeepResearchAgent(Tools(vector, bm25))


# Global agent instance loaded on startup
agent = initialize_system()

# 3. Chat Logic
def chat_fn(message, history):
    # Gradio passes history as a list of dictionaries or tuples
    # Your updated agent.py handles this automatically now
    return agent.run(message, history=history)

# 4. Create and Launch the Interface
# 4. Create and Launch the Interface
demo = gr.ChatInterface(
    fn=chat_fn,
    title="📚 Vivek's RAG System",
    description="Ask questions about your PDFs in data/pdfs.",
    # FIX: Wrap each example string in its own list
    examples=[
        ["What is the main topic of these documents?"], 
        ["Summarize the key points."]
    ]
)

if __name__ == "__main__":
    demo.launch(server_port=7860)


