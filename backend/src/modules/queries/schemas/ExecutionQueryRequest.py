from pydantic import BaseModel
from typing import Optional

from src.modules.queries.schemas.DatabaseConnection import DatabaseConnection


class ExecutionQueryRequest(BaseModel):
    query: Optional[str] = None
    connection: Optional[DatabaseConnection] = None
