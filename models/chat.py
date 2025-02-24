from pydantic import BaseModel
import uuid

class ChatSession(BaseModel):
    id: str
    user_id: int

    @staticmethod
    async def get(session_id: str) -> 'ChatSession':
        # 從數據庫中獲取會話
        # 這裡使用假數據作為示例
        return ChatSession(id=session_id, user_id=1)

    @staticmethod
    async def create(user_id: int) -> 'ChatSession':
        # 創建新的會話並保存到數據庫
        # 這裡使用假數據作為示例
        session_id = str(uuid.uuid4())
        return ChatSession(id=session_id, user_id=user_id)