from typing import Any, Dict, List

from src.modules.queries.service import QueryService


class QueryAdapter:
    def __init__(self, query_service: QueryService):
        self.query_service = query_service

    def get_db_structure(self, schema_name: str) -> str:
        return self.query_service.get_db_structure(schema_name=schema_name)

    def execute_query(self, query: str, schema_name: str) -> List[Dict[str, Any]]:
        return self.query_service.execute_query(query, schema_name)
