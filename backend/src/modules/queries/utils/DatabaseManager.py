from sqlalchemy.engine import Engine
from sqlalchemy import create_engine, MetaData, text
from typing import List, Dict, Any

from src.modules.queries.utils.IDatabaseManager import IDatabaseManager

class DatabaseManager(IDatabaseManager):
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self._engine: Engine = self._connect()
    
    def _connect(self) -> Engine:
        return create_engine(self.connection_string)
    
    def get_engine(self) -> Engine:
        return self._engine
    
    def get_db_structure(self) -> str:
        metadata = MetaData()
        metadata.reflect(bind=self._engine)

        structure = [
            f"Table: {table.name}, Columns: {', '.join(f'{col.name} ({col.type})' for col in table.columns)}"
            for table in metadata.tables.values()
        ]

        return "\n".join(structure)
    
    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        with self._engine.connect() as connection:
            result = connection.execute(text(query))
            columns = result.keys()
            return [dict(zip(columns, row)) for row in result.fetchall()]