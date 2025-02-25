from sqlalchemy.engine import Engine
from src.modules.queries.utils.DatabaseManager import DatabaseManager
from src.modules.queries.service import QueryService
from src.adapters.queries.QueryAdapter import QueryAdapter
from src.modules.text_to_sql.utils.LLMClient import LLMClient
from src.modules.text_to_sql.service import LangToSqlService
from src.config.constants import Settings

from fastapi import Depends


def get_db_manager() -> Engine:
    return DatabaseManager(Settings.DB_URL)


def get_query_service(db_manager: DatabaseManager = Depends(get_db_manager)) -> QueryService:
    return QueryService(db_manager)


def get_query_adapter() -> QueryAdapter:
    return QueryAdapter(Settings.BASE_URL)


def get_llm_client() -> LLMClient:
    return LLMClient()


def get_lang_to_sql_service(query_adapter: QueryAdapter = Depends(get_query_adapter), llm_client: LLMClient = Depends(get_llm_client)) -> LangToSqlService:
    return LangToSqlService(query_adapter, llm_client)
