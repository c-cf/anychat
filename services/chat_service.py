from typing import Optional
from core.rag.rag_manager import RAGManager
from core.document.document_processor import DocumentProcessor
from models.chat import ChatSession
from models.chat_history import ChatHistory

class ChatService:
    def __init__(
        self,
        rag_manager: RAGManager,
        doc_processor: DocumentProcessor
    ):
        self.rag_manager = rag_manager
        self.doc_processor = doc_processor

    async def process_message(
        self,
        user_id: int,
        message: str,
        session_id: Optional[str] = None
    ):
        # 獲取或創建會話
        session = await self._get_or_create_session(user_id, session_id)
        
        # 處理查詢
        rag_response = await self.rag_manager.process_query(message)
        
        # 保存會話歷史
        await self._save_chat_history(
            session_id=session.id,
            message=message,
            response=rag_response
        )
        
        return {
            "answer": rag_response.answer,
            "sources": [
                {
                    "content": doc.content,
                    "metadata": doc.metadata,
                    "relevance_score": doc.score
                }
                for doc in rag_response.sources
            ],
            "session_id": session.id
        }

    async def _get_or_create_session(
        self,
        user_id: int,
        session_id: Optional[str]
    ) -> ChatSession:
        if session_id:
            return await ChatSession.get(session_id)
        return await ChatSession.create(user_id=user_id)

    async def _save_chat_history(
        self,
        session_id: str,
        message: str,
        response: dict
    ):
        await ChatHistory.save(session_id, message, response)