from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

class AlertInput(BaseModel):
    notification_emails: List[EmailStr]
    prompt: str
    expiration_date: datetime
    user: str

class AlertDB(AlertInput):
    sql_query: str
    id: Optional[str] = Field(alias="_id")
    creation_date: datetime = Field(default_factory=datetime.utcnow)