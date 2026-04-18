"""
Vector Store — implements RAG retrieval using FAISS + sentence-transformers.
Falls back to simple keyword search if dependencies not installed.
"""
from src.pdf_processor import chunk_text


class VectorStore:
    """
    Stores document chunks as embeddings and retrieves top-k relevant chunks.
    Uses FAISS for similarity search and sentence-transformers for embeddings.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.chunks: list[str] = []
        self.index = None
        self.model = None
        self._try_load_model(model_name)

    def _try_load_model(self, model_name: str):
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(model_name)
        except ImportError:
            pass  # Will use keyword fallback

    def add_document(self, text: str):
        """Chunk text and add to vector index."""
        self.chunks = chunk_text(text, chunk_size=400, overlap=50)
        if self.model:
            self._build_faiss_index()

    def _build_faiss_index(self):
        try:
            import faiss
            import numpy as np
            embeddings = self.model.encode(self.chunks, show_progress_bar=False)
            embeddings = embeddings.astype("float32")
            dim = embeddings.shape[1]
            self.index = faiss.IndexFlatL2(dim)
            self.index.add(embeddings)
        except ImportError:
            pass  # FAISS not installed, fallback to keyword

    def search(self, query: str, top_k: int = 4) -> str:
        """Return top-k most relevant chunks as a single context string."""
        if not self.chunks:
            return "No document loaded."

        if self.model and self.index is not None:
            return self._faiss_search(query, top_k)
        else:
            return self._keyword_search(query, top_k)

    def _faiss_search(self, query: str, top_k: int) -> str:
        import numpy as np
        q_emb = self.model.encode([query]).astype("float32")
        distances, indices = self.index.search(q_emb, min(top_k, len(self.chunks)))
        results = [self.chunks[i] for i in indices[0] if i < len(self.chunks)]
        return "\n\n---\n\n".join(results)

    def _keyword_search(self, query: str, top_k: int) -> str:
        """Simple TF-based keyword search as fallback."""
        query_words = set(query.lower().split())
        scored = []
        for chunk in self.chunks:
            chunk_words = set(chunk.lower().split())
            score = len(query_words & chunk_words)
            scored.append((score, chunk))
        scored.sort(key=lambda x: x[0], reverse=True)
        top_chunks = [c for _, c in scored[:top_k] if _ > 0]
        if not top_chunks:
            top_chunks = self.chunks[:top_k]
        return "\n\n---\n\n".join(top_chunks)
