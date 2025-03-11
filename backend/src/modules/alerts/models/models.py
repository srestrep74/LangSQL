from pydantic import BaseModel, EmailStr
from typing import List
from datetime import datetime

class AlertInput(BaseModel):
    notification_emails: List[EmailStr]
    prompt: str
    expiration_date: datetime

class AlertDB(AlertInput):
    sql_query: str
    user: str
    creation_date: datetime = datetime.utcnow()