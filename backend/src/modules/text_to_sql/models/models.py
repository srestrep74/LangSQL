from pydantic import BaseModel
from typing import List
from datetime import datetime


class GenerateSyntheticDataRequest(BaseModel):
    schema_name: str
    iterations: int

class Message(BaseModel):
    """Role will be 1 if the message is sended by an user, otherwise will be a 0."""
    role: int
    message: str
    timestamp: datetime

class Chat(BaseModel):
    user_id: str
    messages: List[Message] = []
