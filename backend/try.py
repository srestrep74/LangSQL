from src.modules.text_to_sql.service import LangToSqlService
from src.modules.queries.service import QueryService
from src.modules.text_to_sql.utils.LLMClient import LLMClient
from src.modules.queries.utils.DatabaseManager import DatabaseManager
from src.adapters.queries.QueryAdapter import QueryAdapter

DB_URL = "postgresql://postgres:rposebas2004@localhost:3306/product_db"

db_manager = DatabaseManager(DB_URL)
query_service = QueryService(db_manager)
query_adapter = QueryAdapter(query_service)
llm_client = LLMClient()
llm_service = LangToSqlService(query_adapter, llm_client)
llm_service.conversation()