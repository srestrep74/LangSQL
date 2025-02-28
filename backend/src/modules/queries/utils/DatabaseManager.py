from typing import List, Dict, Any

from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.engine import Engine

from src.modules.queries.utils.IDatabaseManager import IDatabaseManager


class DatabaseManager(IDatabaseManager):
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self._engine: Engine = self._connect()

    def _connect(self) -> Engine:
        return create_engine(self.connection_string)

    def get_engine(self) -> Engine:
        return self._engine

    def get_db_structure(self) -> Dict[str, Any]:
        metadata = MetaData()
        metadata.reflect(bind=self._engine)

        db_structure = {}

        for table in metadata.sorted_tables:
            columns = [
                {
                    "name": col.name,
                    "type": str(col.type),
                    "nullable": col.nullable,
                    "primary_key": col.primary_key,
                }
                for col in table.columns
            ]
            foreign_keys = [
                {
                    "column": fk.parent.name,
                    "references": fk.column.table.name,
                    "referenced_column": fk.column.name,
                }
                for fk in table.foreign_keys
            ]
            db_structure[table.name] = {"columns": columns, "foreign_keys": foreign_keys}

        return db_structure

    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        with self._engine.connect() as connection:
            result = connection.execute(text(query))
            columns = result.keys()
            return [dict(zip(columns, row)) for row in result.fetchall()]