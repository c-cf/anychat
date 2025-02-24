from typing import List, Dict, Optional
from pydantic import BaseModel
from core.vector_store.base import VectorStoreInterface
from core.llm.base import LLMInterface

class Document(BaseModel):
    content: str
    metadata: Dict
    score: Optional[float] = None

class RAGResponse(BaseModel):
    answer: str
    sources: List[Document]
    context_used: str

class RAGManager:
    def __init__(
        self,
        vector_store: VectorStoreInterface,
        llm: LLMInterface,
        max_context_length: int = 4000,
        num_documents: int = 3
    ):
        self.vector_store = vector_store
        self.llm = llm
        self.max_context_length = max_context_length
        self.num_documents = num_documents

    async def _retrieve_relevant_docs(self, query: str) -> List[Document]:
        docs = await self.vector_store.search(
            query=query,
            limit=self.num_documents
        )
        return [Document(**doc) for doc in docs]

    def _prepare_context(self, docs: List[Document]) -> str:
        context_parts = []
        current_length = 0
        
        for doc in docs:
            doc_content = f"文件內容: {doc.content}\n來源: {doc.metadata.get('source', 'unknown')}\n"
            if current_length + len(doc_content) <= self.max_context_length:
                context_parts.append(doc_content)
                current_length += len(doc_content)
            else:
                break
                
        return "\n".join(context_parts)

    def _create_prompt(self, query: str, context: str) -> str:
        return f"""請基於以下提供的文件內容回答問題。如果無法從文件中找到答案，請明確說明。

相關文件內容：
{context}

問題：{query}

請提供準確、簡潔的回答，並引用相關的文件來源。"""

    async def process_query(self, query: str) -> RAGResponse:
        # 1. 檢索相關文檔
        relevant_docs = await self._retrieve_relevant_docs(query)
        
        # 2. 準備上下文
        context = self._prepare_context(relevant_docs)
        
        # 3. 生成提示詞
        prompt = self._create_prompt(query, context)
        
        # 4. 獲取LLM回答
        answer = await self.llm.generate(prompt)
        
        return RAGResponse(
            answer=answer,
            sources=relevant_docs,
            context_used=context
        ) 