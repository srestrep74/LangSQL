from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.engine import Engine
from typing import List, Dict, Any

import re

class QueryService:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.engine: Engine = self._connect()
    
    def _connect(self) -> Engine:
        return create_engine(self.connection_string)

    def get_db_structure(self) -> str:
        metadata = MetaData()
        metadata.reflect(bind=self.engine)

        structure = []
        for table in metadata.tables.values():
            columns = [f"{column.name} ({column.type})" for column in table.columns]
            structure.append(f"Table: {table.name}, Columns: {', '.join(columns)}")
        
        return "\n".join(structure)

    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        query = self.clean_sql_query(query)
        with self.engine.connect() as connection:
            result = connection.execute(text(query))
            columns = result.keys()
            return [dict(zip(columns, row)) for row in result.fetchall()]
    
    def clean_sql_query(self,query) -> str:
        return re.sub(r'```[a-zA-Z]*', '', query).strip()