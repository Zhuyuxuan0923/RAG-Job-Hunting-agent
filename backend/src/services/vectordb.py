from typing import List, Dict, Any
import chromadb
from chromadb.config import Settings as ChromaSettings
from src.config import settings
from src.services.embeddings import embed_texts, embed_query


class VectorStore:
    def __init__(self, client: chromadb.Client = None):
        if client:
            self.client = client
        else:
            self.client = chromadb.Client(ChromaSettings(
                persist_directory=settings.chroma_persist_dir,
                anonymized_telemetry=False,
            ))

    def _get_or_create(self, name: str):
        try:
            return self.client.get_collection(name)
        except Exception:
            return self.client.create_collection(name, metadata={"hnsw:space": "cosine"})

    def add_chunks(self, collection_name: str, chunks: List[Dict[str, Any]], source: str):
        col = self._get_or_create(collection_name)
        texts = [c["text"] for c in chunks]
        embeddings = embed_texts(texts)
        ids = [f"{source}_{c.get('chunk_index', i)}" for i, c in enumerate(chunks)]
        metadatas = []
        for c in chunks:
            meta = {k: str(v) for k, v in c.items() if k != "text"}
            meta["source"] = source
            metadatas.append(meta)
        col.add(embeddings=embeddings, documents=texts, ids=ids, metadatas=metadatas)

    def search(self, collection_name: str, query: str, n_results: int = 20) -> List[Dict[str, Any]]:
        col = self._get_or_create(collection_name)
        q_embedding = embed_query(query)
        results = col.query(query_embeddings=[q_embedding], n_results=n_results)
        out = []
        if results["ids"] and results["ids"][0]:
            for i in range(len(results["ids"][0])):
                item = {
                    "id": results["ids"][0][i],
                    "text": results["documents"][0][i] if results["documents"] else "",
                    "score": results["distances"][0][i] if results["distances"] else 0,
                }
                if results["metadatas"] and results["metadatas"][0]:
                    item.update(results["metadatas"][0][i])
                out.append(item)
        return out

    def clear_collection(self, collection_name: str):
        try:
            self.client.delete_collection(collection_name)
        except Exception:
            pass


COLLECTIONS = ["resume_chunks", "jd_chunks", "interview_exp", "company_info"]
