from typing import Any, Dict, List

from src.modules.queries.schemas.DatabaseConnection import DatabaseConnection
from src.modules.queries.service import QueryService
from src.modules.queries.utils.DatabaseManagerFactory import DatabaseManagerFactory


class QueryAdapter:
    def __init__(self, query_service: QueryService):
        self.query_service = query_service

    def get_db_structure(self, connection: DatabaseConnection) -> Dict[str, Any]:
        return self.query_service.get_db_structure(connection.schema_name)

    def execute_query(self, query: str, connection: DatabaseConnection) -> List[Dict[str, Any]]:
        db_manager = DatabaseManagerFactory.create_manager(connection)
        query_service = QueryService(db_manager)
        return query_service.execute_query(query, connection.schema_name)
