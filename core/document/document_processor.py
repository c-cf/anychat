from typing import List, Dict
from pydantic import BaseModel

class DocumentChunk(BaseModel):
    content: str
    metadata: Dict

class DocumentProcessor:
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_text(self, text: str) -> List[str]:
        chunks = []
        start = 0
        while start < len(text):
            end = start + self.chunk_size
            chunks.append(text[start:end])
            start += self.chunk_size - self.chunk_overlap
        return chunks

    async def process_document(
        self,
        content: str,
        metadata: Dict
    ) -> List[DocumentChunk]:
        texts = self.split_text(content)
        
        chunks = []
        for i, text in enumerate(texts):
            chunk_metadata = {
                **metadata,
                "chunk_index": i,
                "total_chunks": len(texts)
            }
            chunks.append(DocumentChunk(
                content=text,
                metadata=chunk_metadata
            ))
            
        return chunks