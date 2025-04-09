from pydantic import BaseModel
from typing import List
from datetime import datetime


class GenerateSyntheticDataRequest(BaseModel):
    schema_name: str
    iterations: int

class Message(BaseModel):
    role: str
    message: str
    timestamp: datetime

class Chat(BaseModel):
    user_id: str
    messages: List[Message]
