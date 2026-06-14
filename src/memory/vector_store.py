"""Vector database / RAG memory layer."""

from __future__ import annotations

import os
from typing import Any

import chromadb
from chromadb.config import Settings


class VectorMemory:
    """Project memory using a vector database."""

    def __init__(self, provider: str | None = None, persist_dir: str | None = None):
        self.provider = provider or os.getenv("VECTOR_DB_PROVIDER", "chroma")
        self.persist_dir = persist_dir or os.getenv("CHROMA_PERSIST_DIR", "./data/chroma")
        self.client = None
        self.collection = None

    def connect(self) -> None:
        """Connect to the vector database."""
        if self.provider == "chroma":
            self.client = chromadb.Client(
                Settings(persist_directory=self.persist_dir, is_persistent=True)
            )
        else:
            raise NotImplementedError(f"Provider {self.provider} not yet implemented")

    def get_or_create_collection(self, name: str) -> Any:
        """Get or create a collection."""
        if self.client is None:
            self.connect()
        self.collection = self.client.get_or_create_collection(name)
        return self.collection

    def add_documents(
        self,
        documents: list[str],
        ids: list[str],
        metadatas: list[dict[str, Any]] | None = None,
    ) -> None:
        """Add documents to memory."""
        if self.collection is None:
            raise RuntimeError("No collection selected")
        self.collection.add(documents=documents, ids=ids, metadatas=metadatas)

    def query(self, query_text: str, n_results: int = 5) -> dict[str, Any]:
        """Query memory for relevant documents."""
        if self.collection is None:
            raise RuntimeError("No collection selected")
        return self.collection.query(query_texts=[query_text], n_results=n_results)


class ProjectMemory(VectorMemory):
    """Project-specific memory for code, ADRs, specs."""

    def __init__(self, project_id: str, **kwargs: Any):
        super().__init__(**kwargs)
        self.project_id = project_id
        self.get_or_create_collection(f"project_{project_id}")


class OrganizationalMemory(VectorMemory):
    """Cross-project organizational memory."""

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.get_or_create_collection("organizational_memory")
