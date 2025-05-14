from typing import List

from pydantic import BaseModel


class GraphRequest(BaseModel):
    table: str
    columns: List[str]
