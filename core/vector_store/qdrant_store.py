from typing import List, Dict, Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams
from sentence_transformers import SentenceTransformer
from .base import VectorStoreInterface

class QdrantStore(VectorStoreInterface):
    def __init__(
        self,
        collection_name: str = "documents",
        url: str = "http://localhost:6333",
        encoder_model: str = "all-MiniLM-L6-v2",
        vector_size: int = 384
    ):
        self.collection_name = collection_name
        self.client = QdrantClient(url=url)
        self.encoder = SentenceTransformer(encoder_model)
        self.vector_size = vector_size
        
        # Ensure the collection exists
        self._ensure_collection()

    def _ensure_collection(self):
        """Ensure the Qdrant collection exists, create if it does not"""
        collections = self.client.get_collections().collections
        exists = any(col.name == self.collection_name for col in collections)
        
        if not exists:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.vector_size,
                    distance=Distance.COSINE
                )
            )

    def _encode_text(self, text: str) -> List[float]:
        """Encode text into a vector"""
        return self.encoder.encode(text).tolist()

    async def add_documents(self, documents: List[Dict]):
        """
        Add documents to the vector store
        
        documents: List[Dict] format:
        [{
            "id": str/int,
            "content": str,
            "metadata": dict
        }]
        """
        points = []
        for doc in documents:
            vector = self._encode_text(doc["content"])
            
            points.append(models.PointStruct(
                id=doc["id"],
                vector=vector,
                payload={
                    "content": doc["content"],
                    **doc.get("metadata", {})
                }
            ))

        # Batch upload points
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

    async def search(
        self,
        query: str,
        limit: int = 5,
        score_threshold: float = 0.7
    ) -> List[Dict]:
        """
        Search for relevant documents
        
        Return format:
        [{
            "content": str,
            "metadata": dict,
            "score": float
        }]
        """
        # Convert query to vector
        query_vector = self._encode_text(query)
        
        # Perform search
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit,
            score_threshold=score_threshold
        )
        
        # Format results
        results = []
        for hit in search_result:
            payload = hit.payload
            results.append({
                "content": payload.pop("content"),
                "metadata": payload,  # Remaining payload as metadata
                "score": hit.score
            })
            
        return results

    async def delete_documents(self, ids: List[str]):
        """Delete documents by specified IDs"""
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=models.PointIdsList(
                points=ids
            )
        )

    async def update_document(self, doc_id: str, content: str, metadata: Optional[Dict] = None):
        """Update document content and metadata"""
        vector = self._encode_text(content)
        
        self.client.upsert(
            collection_name=self.collection_name,
            points=[models.PointStruct(
                id=doc_id,
                vector=vector,
                payload={
                    "content": content,
                    **(metadata or {})
                }
            )]
        )

    async def get_document(self, doc_id: str) -> Optional[Dict]:
        """Retrieve a single document"""
        points = self.client.retrieve(
            collection_name=self.collection_name,
            ids=[doc_id]
        )
        
        if not points:
            return None
            
        point = points[0]
        payload = point.payload
        return {
            "content": payload.pop("content"),
            "metadata": payload
        }
