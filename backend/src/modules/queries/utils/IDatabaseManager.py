from typing import Protocol
from sqlalchemy.engine import Engine


class IDatabaseManager(Protocol):
    def get_engine(self) -> Engine:
        ...

    def get_db_structure(self, schema_name: str) -> str:
        ...
