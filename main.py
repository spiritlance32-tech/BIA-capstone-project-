from src.document_loader import load_documents
from src.chunking import chunk_text
from src.vector_index import VectorIndex
from src.bm25_index import BM25Index
from src.tools import Tools
from src.agent import DeepResearchAgent


def main():

    print("\n📚 Agentic RAG System Starting...\n")

    # -----------------------------
    # Load Documents
    # -----------------------------
    docs = load_documents()

    if not docs:
        print("⚠️ No documents found. Please add PDFs before running.")
        return

    print(f"Loaded {len(docs)} documents")

    # -----------------------------
    # Chunk Documents
    # -----------------------------
    print("Chunking documents...")

    chunks = []
    for d in docs:
        chunks.extend(chunk_text(d))

    print(f"Created {len(chunks)} chunks")

    # -----------------------------
    # Build Vector Index
    # -----------------------------
    print("Building vector index...")

    vector = VectorIndex()
    vector.build(chunks)

    # -----------------------------
    # Build BM25 Index
    # -----------------------------
    print("Building BM25 index...")

    bm25 = BM25Index()
    bm25.build(chunks)

    # -----------------------------
    # Create Agent
    # -----------------------------
    tools = Tools(vector, bm25)
    agent = DeepResearchAgent(tools)

    print("\n🤖 Agent Ready!")
    print("Type 'exit' to quit\n")

    # -----------------------------
    # Chat Loop
    # -----------------------------
    while True:

        q = input("❓ Question: ").strip()

        if not q:
            print("Please enter a question.")
            continue

        if q.lower() in ["exit", "quit"]:
            print("\nGoodbye 👋")
            break

        try:
            answer = agent.run(q)
            print("\n🤖 Answer:\n")
            print(answer)

        except Exception as e:
            print("\n⚠️ Error:", e)


if __name__ == "__main__":
    main()