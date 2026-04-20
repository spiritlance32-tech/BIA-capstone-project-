
class Tools:

    def __init__(self, vector_index, bm25):

        self.vector = vector_index
        self.bm25 = bm25

    def search_vector(self, query):

        return self.vector.search(query)

    def search_keyword(self, query):

        return self.bm25.search(query)
