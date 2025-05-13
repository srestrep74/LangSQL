from typing import Optional

from pydantic import BaseModel

from src.modules.queries.schemas.DatabaseConnection import DatabaseConnection


class ExecutionQueryRequest(BaseModel):
    query: Optional[str] = None
    connection: Optional[DatabaseConnection] = None
