from typing import Any, Dict, List, Optional

from src.modules.queries.utils.IDatabaseManager import IDatabaseManager
from src.modules.queries.utils.SQLUtils import SQLUtils


class QueryService:
    def __init__(self, db_manager: IDatabaseManager):
        self.db_manager = db_manager

    def get_db_structure(self, schema_name: Optional[str] = None) -> Dict[str, Any]:
        return self.db_manager.get_db_structure(schema_name)

    def execute_query(self, query: str, schema_name: Optional[str] = None) -> List[Dict[str, Any]]:
        query = SQLUtils.clean_sql_query(query)
        return self.db_manager.execute_query(query, schema_name)
