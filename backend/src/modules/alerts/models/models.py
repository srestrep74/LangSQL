from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr


class AlertCreate(BaseModel):
    """
    Data model for creating a new alert.

    This model is used when a new alert is being created and doesn't have an ID yet. By separating the creation model
    from the general alert model, it ensures that the ID is not provided or altered during the creation process.
    """
    notification_emails: List[EmailStr]
    prompt: str
    expiration_date: datetime
    sql_query: Optional[str] = None
    creation_date: datetime = datetime.utcnow()


class Alert(AlertCreate):
    """
    Data model for an existing alert.

    This model extends the AlertCreate model by including an ID attribute. It's used when an alert is being
    fetched or deleted. The separation ensures that the ID is always present for existing alerts,
    making it clear when an alert is new (without an ID) versus when it's an existing alert (with an ID).
    """
    id: str


class AlertPatch(BaseModel):
    """
    Data model for partially updating an existing alert.

    This model is used when an existing alert is being updated with partial data. By providing only the fields
    that need updating, the model ensures that unnecessary changes are not made to the alert in the database.
    """
    notification_emails: Optional[List[EmailStr]] = None
    prompt: Optional[str] = None
    expiration_date: Optional[datetime] = None
