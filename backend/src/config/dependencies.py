from fastapi import Depends

from src.adapters.queries.QueryAdapter import QueryAdapter
from src.adapters.text_to_sql.adapter import TextToSQLAdapter
from src.modules.queries.schemas.DatabaseConnection import DatabaseConnection
from src.modules.queries.service import QueryService
from src.modules.queries.utils.DatabaseManagerFactory import DatabaseManagerFactory
from src.modules.queries.utils.IDatabaseManager import IDatabaseManager
from src.modules.text_to_sql.repositories.repository import TextToSqlRepository
from src.modules.text_to_sql.service import LangToSqlService, SyntheticDataModelService
from src.modules.text_to_sql.utils.APIClientLLMClient import APIClientLLMClient
from src.modules.text_to_sql.utils.ILLMCLient import ILLMClient
from src.modules.text_to_sql.utils.LangChainLLMClient import LangChainLLMClient
from src.modules.reports.service import ReportService
from src.modules.reports.repositories.repository import ReportRepository


def get_db_manager(connection: DatabaseConnection) -> IDatabaseManager:
    return DatabaseManagerFactory.create_manager(connection)


def get_query_service(db_manager: IDatabaseManager = Depends(get_db_manager)) -> QueryService:
    return QueryService(db_manager)


def get_query_adapter(query_service: QueryService = Depends(get_query_service)) -> QueryAdapter:
    return QueryAdapter(query_service)


def get_langchain_llm_client() -> ILLMClient:
    return LangChainLLMClient()


def get_apiclient_llm_client() -> ILLMClient:
    return APIClientLLMClient()


def get_text_to_sql_repository() -> TextToSqlRepository:
    return TextToSqlRepository()


def get_lang_to_sql_service(query_adapter: QueryAdapter = Depends(get_query_adapter), llm_client: ILLMClient = Depends(get_langchain_llm_client), repository: TextToSqlRepository = Depends(get_text_to_sql_repository)) -> LangToSqlService:
    return LangToSqlService(query_adapter, llm_client, repository)


def get_synthetic_data_model_service(query_adapter: QueryAdapter = Depends(get_query_adapter), llm_client: ILLMClient = Depends(get_apiclient_llm_client)) -> SyntheticDataModelService:
    return SyntheticDataModelService(query_adapter, llm_client)


def get_text_to_sql_adapter(lang_to_sql_service: LangToSqlService = Depends(get_lang_to_sql_service)):
    return TextToSQLAdapter(lang_to_sql_service)


def get_report_repository() -> ReportRepository:
    return ReportRepository()


def get_report_service(query_adapter: QueryAdapter = Depends(get_query_adapter)) -> ReportService:
    report_repository = get_report_repository()
    return ReportService(report_repository, query_adapter)
