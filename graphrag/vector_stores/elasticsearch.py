# Copyright (c) 2024 CChu ML.
# Licensed under the MIT License

"""A package containing the Elasticsearch vector store implementation."""

import json
from typing import Any

from elasticsearch import Elasticsearch, NotFoundError

from graphrag.data_model.types import TextEmbedder
from graphrag.vector_stores.base import (
    DEFAULT_VECTOR_SIZE,
    BaseVectorStore,
    VectorStoreDocument,
    VectorStoreSearchResult,
)


class ElasticsearchVectorStore(BaseVectorStore):
    """Elasticsearch vector store implementation."""

    es_client: Elasticsearch | None = None

    def __init__(
        self, 
        index_name: str, 
        vector_field: str = "vector",
        es_url: str | None = None, 
        es_api_key: str | None = None,
        vector_size: int = DEFAULT_VECTOR_SIZE,
        **kwargs
    ):
        """
        Initialize ElasticsearchVectorStore.
        
        Args:
            index_name: ES index name
            vector_field: Vector field name
            es_url: ES connection URL
            es_api_key: ES API key
            vector_size: Vector dimension size
            **kwargs: Additional parameters
        """
        self.index_name = index_name
        self.vector_field = vector_field
        self.vector_size = vector_size
        
        # Connect immediately if URL is provided
        if es_url:
            self.es_client = Elasticsearch(hosts=es_url, api_key=es_api_key, **kwargs)
            self._ensure_index_exists()

    def connect(self, **kwargs: Any) -> None:
        """Connect to Elasticsearch."""
        self.es_client = Elasticsearch(**kwargs)
        self._ensure_index_exists()

    def _ensure_index_exists(self) -> None:
        """Ensure the index exists and is properly configured."""
        if self.es_client is None:
            msg = "Elasticsearch client is not initialized."
            raise ValueError(msg) from None
            
        # Check if the index exists
        if not self.es_client.indices.exists(index=self.index_name):
            # Create the index and configure vector search
            mappings = {
                "mappings": {
                    "properties": {
                        "id": {"type": "keyword"},
                        "text": {"type": "text"},
                        self.vector_field: {
                            "type": "dense_vector",
                            "dims": self.vector_size,
                            "index": True,
                            "similarity": "cosine"
                        },
                        "attributes": {"type": "text"}
                    }
                }
            }
            self.es_client.indices.create(index=self.index_name, body=mappings)

    def load_documents(
        self, documents: list[VectorStoreDocument], overwrite: bool = True
    ) -> None:
        """Load documents into the vector store."""
        if self.es_client is None:
            msg = "Elasticsearch client is not initialized."
            raise ValueError(msg) from None
        
        # Bulk operations are more efficient
        bulk_data = []
        for doc in documents:
            # Index operation
            index_op = {
                "_index": self.index_name,
                "_id": str(doc.id),
                "_source": {
                    "id": doc.id,
                    "text": doc.text,
                    self.vector_field: doc.vector,
                    "attributes": json.dumps(doc.attributes),
                }
            }
            bulk_data.append(index_op)
            
        if bulk_data:
            # Use bulk API for batch import
            from elasticsearch.helpers import bulk
            bulk(self.es_client, bulk_data)

    def _search_by_vector(self, query_embedding: list[float], k: int) -> list[dict]:
        """Perform search by vector."""
        if self.es_client is None:
            msg = "Elasticsearch client is not initialized."
            raise ValueError(msg)
            
        # Construct vector query
        query = {
            "knn": {
                self.vector_field: {
                    "vector": query_embedding,
                    "k": k
                }
            }
        }
        
        # Execute search
        result = self.es_client.search(
            index=self.index_name,
            body={"query": query},
            size=k
        )
        
        # Parse results
        hits = result.get("hits", {}).get("hits", [])
        search_results = []
        
        for hit in hits:
            source = hit.get("_source", {})
            search_results.append({
                "id": source.get("id", ""),
                "text": source.get("text", ""),
                "vector": source.get(self.vector_field, []),
                "attributes": source.get("attributes", "{}"),
                "SimilarityScore": hit.get("_score", 0.0)
            })
            
        return search_results

    def similarity_search_by_vector(
        self, query_embedding: list[float], k: int = 10, **kwargs: Any
    ) -> list[VectorStoreSearchResult]:
        """Perform vector similarity search."""
        items = self._search_by_vector(query_embedding, k)
        return [
            VectorStoreSearchResult(
                document=VectorStoreDocument(
                    id=item.get("id", ""),
                    text=item.get("text", ""),
                    vector=item.get("vector", []),
                    attributes=(json.loads(item.get("attributes", "{}"))),
                ),
                score=item.get("SimilarityScore", 0.0),
            )
            for item in items
        ]

    def similarity_search_by_text(
        self, text: str, text_embedder: TextEmbedder, k: int = 10, **kwargs: Any
    ) -> list[VectorStoreSearchResult]:
        """Perform similarity search by text."""
        query_embedding = text_embedder(text)
        if query_embedding:
            return self.similarity_search_by_vector(
                query_embedding=query_embedding, k=k
            )
        return []

    def filter_by_id(self, include_ids: list[str] | list[int]) -> dict:
        """Construct query to filter by ID."""
        return {"ids": {"values": [str(id) for id in include_ids]}}

    def search_by_id(self, id: str) -> VectorStoreDocument:
        """Search document by ID."""
        if self.es_client is None:
            msg = "Elasticsearch client is not initialized."
            raise ValueError(msg)

        try:
            response = self.es_client.get(index=self.index_name, id=str(id))
            source = response.get("_source", {})
            
            return VectorStoreDocument(
                id=response.get("_id", ""),
                vector=source.get(self.vector_field, []),
                text=source.get("text", ""),
                attributes=(json.loads(source.get("attributes", "{}"))),
            )
        except NotFoundError as e:
            msg = f"Error retrieving document with ID {id}: {e!s}"
            raise ValueError(msg) from None