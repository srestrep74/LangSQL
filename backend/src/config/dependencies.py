from sqlalchemy.engine import Engine
from src.modules.queries.utils.DatabaseManager import DatabaseManager
from src.modules.queries.service import QueryService
from src.adapters.queries.QueryAdapter import QueryAdapter
from src.modules.text_to_sql.service import LangToSqlService, SyntheticDataModelService
from src.config.constants import Settings
from src.modules.text_to_sql.utils.ILLMCLient import ILLMClient
from src.modules.text_to_sql.utils.LangChainLLMClient import LangChainLLMClient
from src.modules.text_to_sql.utils.APIClientLLMClient import APIClientLLMClient


from fastapi import Depends


def get_db_manager() -> Engine:
    return DatabaseManager(Settings.DB_URL)


def get_query_service(db_manager: DatabaseManager = Depends(get_db_manager)) -> QueryService:
    return QueryService(db_manager)


def get_query_adapter(query_service: QueryService = Depends(get_query_service)) -> QueryAdapter:
    return QueryAdapter(query_service)


def get_langchain_llm_client() -> ILLMClient:
    return LangChainLLMClient()

def get_apiclient_llm_client() -> ILLMClient:
    return APIClientLLMClient()

def get_lang_to_sql_service(query_adapter: QueryAdapter = Depends(get_query_adapter), llm_client: ILLMClient = Depends(get_langchain_llm_client)) -> LangToSqlService:
    return LangToSqlService(query_adapter, llm_client)


def get_synthetic_data_model_service(query_adapter: QueryAdapter = Depends(get_query_adapter), llm_client: ILLMClient = Depends(get_apiclient_llm_client)) -> SyntheticDataModelService:
    return SyntheticDataModelService(query_adapter, llm_client)
