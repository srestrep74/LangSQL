from typing import Any, Dict, List, Iterator
from contextlib import contextmanager

from sqlalchemy import MetaData, create_engine, text
from sqlalchemy.engine import Engine, Connection

from src.modules.queries.utils.IDatabaseManager import IDatabaseManager


class DatabaseManager(IDatabaseManager):
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self._engine: Engine = create_engine(
            self.connection_string,
            pool_pre_ping = True,
            pool_recycle = 3600,
            pool_size = 5,
            max_overflow = 10
        )

    @contextmanager
    def _get_connection(self) -> Iterator[Connection]:
        conn = self._engine.connect()
        try:
            yield conn
        finally:
            conn.close()

    def get_db_structure(self, schema_name: str) -> Dict[str, Any]:
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
                    "columns": columns, "foreign_keys": foreign_keys}

            return db_structure

    def execute_query(self, query: str, schema_name: str) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            transaction = conn.begin()
            try:
                conn.execute(text(f"SET search_path TO {schema_name}"))
                result = conn.execute(text(query))
                transaction.commit()

                if result.returns_rows:
                    columns = result.keys()
                    return [dict(zip(columns, row)) for row in result.fetchall()]
                else:
                    return [{"message": "Query executed successfully"}]
            except Exception as e:
                transaction.rollback()
                raise e
