from pydantic import BaseModel

from src.modules.queries.schemas.DatabaseConnection import DatabaseConnection


class ExecutionQueryRequest(BaseModel):
    query: str
    connection: DatabaseConnection
