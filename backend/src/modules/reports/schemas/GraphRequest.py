from pydantic import BaseModel
from typing import List


class GraphRequest(BaseModel):
    table: str
    columns: List[str]
