from typing import Optional

from pydantic import BaseModel

from src.modules.queries.utils.DatabaseType import DatabaseType


class DatabaseConnection(BaseModel):
    db_type: DatabaseType
    username: str
    password: str
    host: str
    port: int
    database_name: str
    schema_name: Optional[str] = None
