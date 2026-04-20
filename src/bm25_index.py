from rank_bm25 import BM25Okapi


class BM25Index:

    def __init__(self):
        self.bm25 = None
        self.chunks = []

    def build(self, chunks):
        self.chunks = chunks

        # Better tokenization (lowercase helps a lot)
        corpus = [c.lower().split() for c in chunks]

        self.bm25 = BM25Okapi(corpus)

    def search(self, query, k=5):
        if self.bm25 is None:
            return []

        tokens = query.lower().split()

        scores = self.bm25.get_scores(tokens)

        ranked = sorted(
            list(enumerate(scores)),
            key=lambda x: x[1],
            reverse=True
        )

        results = []

        for idx, score in ranked[:k]:
            results.append({
                "text": self.chunks[idx],
                "score": float(score)
            })

        return results