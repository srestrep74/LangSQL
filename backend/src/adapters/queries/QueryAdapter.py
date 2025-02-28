from typing import List, Dict, Any
from src.modules.queries.service import QueryService


class QueryAdapter:
    def __init__(self, query_service: QueryService):
        self.query_service = query_service

    def get_db_structure(self) -> str:
        return self.query_service.get_db_structure()

    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        return self.query_service.execute_query(query)
