from typing import List
from core.vector_store.base import VectorStoreInterface
from core.db.base import DatabaseInterface

class DocumentService:
    def __init__(self, db: DatabaseInterface, vector_store: VectorStoreInterface):
        self.db = db
        self.vector_store = vector_store

    async def add_document(self, content: str, metadata: dict):
        doc_id = await self.db.execute(
            "INSERT INTO documents (content, metadata) VALUES (?, ?)",
            {"content": content, "metadata": metadata}
        )
        
        await self.vector_store.add_documents([{
            "id": doc_id,
            "content": content,
            "metadata": metadata
        }])

    async def list_documents(self, user_id: str) -> List[dict]:
        documents = await self.db.execute(
            "SELECT * FROM documents WHERE user_id = ?",
            {"user_id": user_id}
        )
        return documents
    
    async def get_document(self, document_id: str, user_id: str) -> dict:
        document = await self.db.execute(
            "SELECT * FROM documents WHERE id = ? AND user_id = ?",
            {"id": document_id, "user_id": user_id},
            one=True
        )
        return document
    
    async def update_document(self, document_id: str, content: str, metadata: dict, user_id: str):
        await self.db.execute(
            "UPDATE documents SET content = ?, metadata = ? WHERE id = ? AND user_id = ?",
            {"content": content, "metadata": metadata, "id": document_id, "user_id": user_id}
        )
        
        await self.vector_store.update_document(document_id, content, metadata)

    async def delete_document(self, document_id: str, user_id: str):
        await self.db.execute(
            "DELETE FROM documents WHERE id = ? AND user_id = ?",
            {"id": document_id, "user_id": user_id}
        )
        
        await self.vector_store.delete_document(document_id)