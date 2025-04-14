from pydantic import BaseModel
from typing import Optional

from src.modules.text_to_sql.models.models import Chat

class ChatRequest(BaseModel):
    user_input: str
    schema_name: str
    chat_data: Chat
    chat_id: Optional[str] = None
