import json
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from app.core.config import settings


class KnowledgeIndex:
    def __init__(self) -> None:
        self.model = SentenceTransformer(settings.embedding_model)
        self.index: faiss.IndexFlatL2 | None = None
        self.metadata: list[dict] = []

    def load(self) -> None:
        index_path = Path(settings.vector_index_path)
        metadata_path = Path(settings.vector_metadata_path)
        index_path.parent.mkdir(parents=True, exist_ok=True)
        metadata_path.parent.mkdir(parents=True, exist_ok=True)

        if index_path.exists() and metadata_path.exists():
            self.index = faiss.read_index(str(index_path))
            self.metadata = json.loads(metadata_path.read_text(encoding="utf-8"))

    def _ensure_index(self, dimension: int) -> None:
        if self.index is None:
            self.index = faiss.IndexFlatL2(dimension)

    def _persist(self) -> None:
        if self.index is None:
            return
        faiss.write_index(self.index, settings.vector_index_path)
        Path(settings.vector_metadata_path).write_text(json.dumps(self.metadata, indent=2), encoding="utf-8")

    def add_document(self, document_id: int, title: str, chunks: list[str]) -> None:
        if not chunks:
            return
        embeddings = self.model.encode(chunks, convert_to_numpy=True, normalize_embeddings=True)
        embeddings = embeddings.astype("float32")
        self._ensure_index(embeddings.shape[1])
        self.index.add(embeddings)
        for chunk in chunks:
            self.metadata.append(
                {"document_id": document_id, "document_title": title, "chunk_text": chunk}
            )
        self._persist()

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        if self.index is None or not self.metadata:
            return []
        query_vector = self.model.encode([query], convert_to_numpy=True, normalize_embeddings=True).astype("float32")
        distances, indices = self.index.search(query_vector, top_k)
        results: list[dict] = []
        for distance, idx in zip(distances[0], indices[0], strict=False):
            if idx < 0 or idx >= len(self.metadata):
                continue
            item = self.metadata[idx].copy()
            item["score"] = float(1 / (1 + distance))
            results.append(item)
        return results


knowledge_index = KnowledgeIndex()
