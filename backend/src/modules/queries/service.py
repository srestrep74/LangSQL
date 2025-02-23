from sqlalchemy.engine import Engine
from typing import List, Dict, Any

from src.modules.queries.utils.IDatabaseManager import IDatabaseManager
from src.modules.queries.utils.SQLUtils import SQLUtils

class QueryService:
    def __init__(self, db_manager: IDatabaseManager):
        self.db_manager = db_manager
        self.engine: Engine = self.db_manager.get_engine()

    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        query = SQLUtils.clean_sql_query(query)
        return self.db_manager.execute_query(query)
    
    def get_db_structure(self) -> str:
        return self.db_manager.get_db_structure()