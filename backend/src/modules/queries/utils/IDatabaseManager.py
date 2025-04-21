from typing import Any, Dict, List, Optional, Protocol

from sqlalchemy.engine import Engine


class IDatabaseManager(Protocol):

    def __init__(self, engine: Engine):
        ...

    def get_db_structure(self, schema_name: Optional[str] = None) -> Dict[str, Any]:
        ...

    def execute_query(self, query: str, schema_name: Optional[str] = None) -> List[Dict[str, Any]]:
        ...

    def get_engine(self) -> Engine:
        ...
