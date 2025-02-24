from pydantic import BaseModel
from typing import Dict

class ChatHistory(BaseModel):
    session_id: str
    message: str
    response: Dict

    @staticmethod
    async def save(session_id: str, message: str, response: Dict):
        # 保存聊天歷史到數據庫
        # 這裡使用假數據作為示例
        pass