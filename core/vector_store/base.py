from abc import ABC, abstractmethod
from typing import List, Dict

class VectorStoreInterface(ABC):
    @abstractmethod
    async def add_documents(self, documents: List[Dict]):
        pass

    @abstractmethod
    async def search(self, query: str, limit: int = 5):
        pass 

    @abstractmethod
    async def update_document(self, document_id: str, content: str, metadata: Dict):
        pass

    @abstractmethod
    async def delete_document(self, document_id: str):
        pass