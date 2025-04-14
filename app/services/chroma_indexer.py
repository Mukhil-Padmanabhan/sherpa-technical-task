import os
from typing import List
import chromadb
from app.config import settings
from app.models.schemas import Document

COLLECTION_PREFIX = "collection_"
class ChromaIndexer:
    """
    A wrapper around ChromaDB that supports tenant-aware document indexing and search.
    Ensures each tenant has an isolated collection.
    """

    def __init__(self):
        self.client = chromadb.HttpClient(host="chroma", port=8000)

        self.collections = {} 

    def _get_collection_name(self, tenant: str) -> str:
        """
        Returns a sanitized, unique collection name for a tenant.
        """
        return f"{COLLECTION_PREFIX}{tenant.lower()}"

    def get_collection(self, tenant: str):
        """
        Retrieves or creates a Chroma collection specific to a tenant.
        """
        if tenant not in self.collections:
            collection_name = self._get_collection_name(tenant)
            try:
                self.collections[tenant] = self.client.get_or_create_collection(name=collection_name)
            except Exception as e:
                raise RuntimeError(f"Failed to get/create collection for tenant '{tenant}': {e}")
        return self.collections[tenant]

    def index_documents(self, tenant: str, docs: List[Document]):
        """
        Splits and adds documents into Chroma under the specified tenant's collection.
        """
        if not docs:
            return

        collection = self.get_collection(tenant)

        for doc in docs:
            chunks = self._chunk_text(doc.content)
            metadatas = [{"file_name": doc.file_name, "doc_id": doc.id} for _ in chunks]
            ids = [f"{doc.id}_{i}" for i in range(len(chunks))]

            try:
                collection.add(documents=chunks, metadatas=metadatas, ids=ids)
            except Exception as e:
                print(f"Error adding doc {doc.file_name} to Chroma: {e}")

    def search(self, tenant: str, query: str, top_k: int = 5):
        """
        Queries the tenant-specific collection with semantic search.
        """
        try:
            collection = self.get_collection(tenant)
            return collection.query(query_texts=[query], n_results=top_k)
        except Exception as e:
            raise RuntimeError(f"Search failed for tenant '{tenant}': {e}")

    def _chunk_text(self, text: str, chunk_size: int = 200) -> List[str]:
        """
        Splits the document text into word-based chunks for better embedding.
        """
        words = text.split()
        return [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
