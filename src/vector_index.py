import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class VectorIndex:
    def __init__(self):
        # Embedding model
        self.model = SentenceTransformer("BAAI/bge-small-en-v1.5")
        self.index = None
        self.chunks = []

    def build(self, chunks):
        if not chunks:
            return

        self.chunks = chunks

        # Encode chunks
        embeddings = self.model.encode(chunks, show_progress_bar=True)
        embeddings = np.array(embeddings).astype("float32")

        # Normalize for cosine similarity
        faiss.normalize_L2(embeddings)

        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dim)
        self.index.add(embeddings)

        print(f"✅ Vector Index built with {len(chunks)} chunks.")

    def search(self, query, k=10, threshold=0.5):
        """
        Improved search:
        - searches more candidates (k=10)
        - filters low-quality results
        - returns top relevant chunks with scores
        """

        if self.index is None:
            return []

        # Expand query (simple but effective)
        queries = [
            query,
            f"Explain {query}",
            f"Details about {query}"
        ]

        all_results = []

        for q_text in queries:
            q = self.model.encode([q_text])
            q = np.array(q).astype("float32")
            faiss.normalize_L2(q)

            distances, idx = self.index.search(q, k)

            for score, i in zip(distances[0], idx[0]):
                if i != -1 and i < len(self.chunks):
                    all_results.append({
                        "text": self.chunks[i],
                        "score": float(score)
                    })

        # Remove duplicates (important)
        seen = set()
        unique_results = []
        for r in all_results:
            if r["text"] not in seen:
                seen.add(r["text"])
                unique_results.append(r)

        # Filter low-quality matches
        filtered = [r for r in unique_results if r["score"] > threshold]

        # Sort by score
        filtered = sorted(filtered, key=lambda x: x["score"], reverse=True)

        # Return top 5
        return filtered[:5]