from contextlib import contextmanager
from typing import Any, Dict, Iterator, List, Optional

from sqlalchemy import MetaData, text
from sqlalchemy.engine import Connection, Engine

from src.modules.queries.utils.IDatabaseManager import IDatabaseManager


class PostgreSQLManager(IDatabaseManager):
    def __init__(self, engine: Engine):
        self._engine = engine

    @contextmanager
    def _get_connection(self) -> Iterator[Connection]:
        conn = self._engine.connect()
        try:
            yield conn
        finally:
            conn.close()

    def get_db_structure(self, schema_name: Optional[str] = None) -> Dict[str, Any]:
        with self._get_connection() as conn:
            metadata = MetaData(schema=schema_name)
            metadata.reflect(bind=conn)

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
                db_structure[table.name] = {
                    "columns": columns,
                    "foreign_keys": foreign_keys
                }
            return db_structure

    def execute_query(self, query: str, schema_name: Optional[str] = None) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            transaction = conn.begin()
            try:
                if schema_name:
                    conn.execute(text(f"SET search_path TO {schema_name}"))
                result = conn.execute(text(query))
                transaction.commit()

                if result.returns_rows:
                    columns = result.keys()
                    return [dict(zip(columns, row)) for row in result.fetchall()]
                return [{"message": "Query executed successfully"}]
            except Exception as e:
                transaction.rollback()
                print(f"Error executing query: {e}")
                raise e

    def get_engine(self) -> Engine:
        return self._engine
