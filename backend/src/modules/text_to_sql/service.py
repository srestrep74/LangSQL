import json
from typing import Dict

from src.adapters.queries.QueryAdapter import QueryAdapter
from src.modules.queries.utils.SQLUtils import SQLUtils
from src.modules.text_to_sql.prompts.synthetic_data import (
    GENERATE_SYNTHETIC_DATA_PROMPT,
)
from src.modules.text_to_sql.utils.ILLMCLient import ILLMClient
from src.modules.queries.schemas.DatabaseConnection import DatabaseConnection


class SyntheticDataModelService:
    def __init__(self, query_adapter: QueryAdapter, llm_client: ILLMClient):
        self.query_adapter = query_adapter
        self.llm_client = llm_client

    def generate_synthetic_data(self, iterations: int, connection: DatabaseConnection) -> str:
        iterations = iterations // 40
        db_structure = self.query_adapter.get_db_structure(connection)
        user_input = GENERATE_SYNTHETIC_DATA_PROMPT.format(
            db_structure=db_structure, schema_name=connection.schema_name)
        last_query = ""

        for _ in range(iterations):
            try:
                last_query = self.llm_client.get_model_response(user_input)
                last_query = SQLUtils.clean_sql_query(last_query)
                self.query_adapter.execute_query(last_query, connection)
            except Exception as e:
                return {"error": str(e)}
        return last_query


class LangToSqlService:
    def __init__(self, query_adapter: QueryAdapter, llm_client: ILLMClient):
        self.query_adapter = query_adapter
        self.llm_client = llm_client

    def process_user_query(self, user_input: str, connection: DatabaseConnection) -> Dict:
        try:
            db_structure = self.query_adapter.get_db_structure(connection)
            sql_query = self.llm_client.get_model_response(
                db_structure, user_input, connection.schema_name)
            sql_results = self.query_adapter.execute_query(sql_query, connection)
            human_response = self.llm_client.get_human_response(user_input)
            response = {
                "header": human_response,
                "sql_query": sql_query,
                "sql_results": json.dumps(sql_results)
            }
            return response
        except Exception as e:
            return {"error": str(e)}

    def get_response(self, user_input: str, connection: DatabaseConnection):
        try:
            db_structure = self.query_adapter.get_db_structure(connection)
            sql_query = self.llm_client.get_model_response(
                db_structure, user_input, connection.schema_name)
            return sql_query
        except Exception as e:
            return {"error": str(e)}
