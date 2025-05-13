import hashlib
from typing import Dict, Type
from urllib.parse import quote_plus

from sqlalchemy import Engine, create_engine

from src.modules.queries.schemas.DatabaseConnection import DatabaseConnection
from src.modules.queries.utils.DatabaseType import DatabaseType
from src.modules.queries.utils.IDatabaseManager import IDatabaseManager


class DatabaseManagerFactory:
    _managers: Dict[DatabaseType, Type[IDatabaseManager]] = {}
    _engine_cache: Dict[str, Engine] = {}

    @classmethod
    def register(cls, db_type: DatabaseType, manager_class: Type[IDatabaseManager]):
        cls._managers[db_type] = manager_class

    @classmethod
    def _get_connection_string(cls, conn_info: DatabaseConnection) -> str:
        password_encoded = quote_plus(conn_info.password)

        if conn_info.db_type == DatabaseType.POSTGRESQL:
            return f"postgresql://{conn_info.username}:{password_encoded}@{conn_info.host}:{conn_info.port}/{conn_info.database_name}"
        elif conn_info.db_type == DatabaseType.MYSQL:
            return f"mysql+pymysql://{conn_info.username}:{password_encoded}@{conn_info.host}:{conn_info.port}/{conn_info.database_name}"

        raise ValueError(f"Unsupported database type: {conn_info.db_type}")

    @classmethod
    def _get_cache_key(cls, conn_info: DatabaseConnection) -> str:
        hash_input = f"{conn_info.db_type}:{conn_info.username}@{conn_info.host}:{conn_info.port}/{conn_info.database_name}"
        return hashlib.sha256(hash_input.encode()).hexdigest()

    @classmethod
    def create_manager(cls, connection_info: DatabaseConnection) -> IDatabaseManager:
        if connection_info.db_type not in cls._managers:
            raise ValueError(f"Unsupported database type: {connection_info.db_type}")

        conn_str = cls._get_connection_string(connection_info)
        cache_key = cls._get_cache_key(connection_info)

        if cache_key not in cls._engine_cache:
            engine = create_engine(
                conn_str,
                pool_pre_ping=True,
                pool_recycle=3600,
                pool_size=5,
                max_overflow=10,
                connect_args={
                    "connect_timeout": 5
                }
            )
            cls._engine_cache[cache_key] = engine

        return cls._managers[connection_info.db_type](cls._engine_cache[cache_key])
