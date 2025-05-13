from pydantic import BaseModel
from typing import List
from src.modules.queries.schemas.DatabaseConnection import DatabaseConnection

class GraphRequest(BaseModel):
    table: str
    columns: List[str]