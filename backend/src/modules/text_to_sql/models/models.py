from pydantic import BaseModel, Field
from typing import List
from datetime import datetime, timezone


class GenerateSyntheticDataRequest(BaseModel):
    schema_name: str
    iterations: int


class Message(BaseModel):
    """Role will be 1 if the message is sent by an user, otherwise will be a 0."""
    role: int
    message: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Chat(BaseModel):
    user_id: str
    messages: List[Message] = []
