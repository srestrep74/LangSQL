from typing import Any, Dict, List, Optional

from pydantic import BaseModel

# User model


class UserPatch(BaseModel):
    """
    Data model for partially updating an existing user.

    This model is used when an existing user is being updated with partial data. By providing only the fields
    that need updating, the model ensures that unnecessary changes are not made to the user in the database.
    """
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    main_credentials: Optional[Dict[str, Any]] = None
    credentials: Optional[List[Dict[str, Any]]] = None
    queries: Optional[List[str]] = None
    alerts: Optional[List[str]] = None


class UserCreate(BaseModel):
    """
    Data model for creating a new user.

    This model is used when a new user is being created and doesn't have an ID yet. By separating the creation model
    from the general user model, it ensures that the ID is not provided or altered during the creation process.
    """
    name: str
    email: str
    password: str
    main_credentials: Dict[str, Any]
    credentials: List[Dict[str, Any]]
    queries: Optional[List[str]] = None
    alerts: Optional[List[str]] = None


class User(UserCreate):
    """
    Data model for an existing user.

    This model extends the UserCreate model by including an ID attribute. It's used when an user is being
    fetched or deleted. The separation ensures that the ID is always present for existing users,
    making it clear when an user is new (without an ID) versus when it's an existing user (with an ID).
    """
    id: str
