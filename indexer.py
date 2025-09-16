# indexer.py
import os
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List
from dotenv import load_dotenv

load_dotenv()

VECTOR_STORE = os.getenv("VECTOR_STORE", "faiss")

try:
    import pinecone
except Exception:
    pinecone = None

# Embedding model
EMBED_MODEL = SentenceTransformer("all-MiniLM-L6-v2")

def embed_texts(texts: List[str]) -> np.ndarray:
    return EMBED_MODEL.encode(texts, convert_to_numpy=True)

# --- FAISS ---
class FaissIndexer:
    def __init__(self):
        import faiss
        self.faiss = faiss
        self.index = None
        self.dim = EMBED_MODEL.get_sentence_embedding_dimension()
        self.ids = []

    def build(self, texts: List[str], metadatas: List[dict]):
        if not texts:
            return
        vectors = embed_texts(texts).astype("float32")
        self.index = self.faiss.IndexFlatIP(self.dim)
        self.faiss.normalize_L2(vectors)
        self.index.add(vectors)
        self.ids = metadatas

    def query(self, query: str, top_k: int = 5) -> List[dict]:
        if self.index is None:
            return []
        qvec = embed_texts([query]).astype("float32")
        self.faiss.normalize_L2(qvec)
        D, I = self.index.search(qvec, top_k)
        return [self.ids[idx] for idx in I[0] if idx < len(self.ids)]

# --- Pinecone ---
class PineconeIndexer:
    def __init__(self, index_name="agentic-index"):
        if pinecone is None:
            raise RuntimeError("pinecone not installed")
        self.index_name = index_name
        api_key = os.getenv("PINECONE_API_KEY")
        env = os.getenv("PINECONE_ENVIRONMENT")
        pinecone.init(api_key=api_key, environment=env)
        if index_name not in pinecone.list_indexes():
            pinecone.create_index(index_name, dimension=EMBED_MODEL.get_sentence_embedding_dimension())
        self.index = pinecone.Index(index_name)

    def upsert(self, texts: List[str], metadatas: List[dict]):
        if not texts:
            return
        vectors = embed_texts(texts).tolist()
        items = [(str(i), vectors[i], metadatas[i]) for i in range(len(texts))]
        self.index.upsert(items)

    def query(self, query: str, top_k: int = 5):
        q = embed_texts([query])[0].tolist()
        res = self.index.query(q, top_k=top_k, include_metadata=True)
        return [item['metadata'] for item in res['matches']]

# Factory
def get_indexer():
    if VECTOR_STORE == "pinecone":
        return PineconeIndexer()
    else:
        return FaissIndexer()
