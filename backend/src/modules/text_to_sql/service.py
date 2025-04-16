import json
from typing import Dict, Optional
from datetime import datetime, timezone

from src.adapters.queries.QueryAdapter import QueryAdapter
from src.modules.queries.utils.SQLUtils import SQLUtils
from src.modules.text_to_sql.prompts.synthetic_data import (
    GENERATE_SYNTHETIC_DATA_PROMPT,
)
from src.modules.text_to_sql.utils.ILLMCLient import ILLMClient
from src.modules.text_to_sql.models.models import Chat, Message
from src.modules.text_to_sql.repositories.repository import TextToSqlRepository


class SyntheticDataModelService:
    def __init__(self, query_adapter: QueryAdapter, llm_client: ILLMClient):
        self.query_adapter = query_adapter
        self.llm_client = llm_client

    def generate_synthetic_data(self, iterations: int, schema_name: str) -> str:
        iterations = iterations // 40
        db_structure = self.query_adapter.get_db_structure(schema_name=schema_name)
        user_input = GENERATE_SYNTHETIC_DATA_PROMPT.format(
            db_structure=db_structure, schema_name=schema_name)
        last_query = ""

        for _ in range(iterations):
            try:
                last_query = self.llm_client.get_model_response(db_structure, user_input)
                last_query = SQLUtils.clean_sql_query(last_query)
                self.query_adapter.execute_query(last_query, schema_name)
            except Exception as e:
                return {"error": str(e)}
        return last_query


class LangToSqlService:
    def __init__(self, query_adapter: QueryAdapter, llm_client: ILLMClient, TextToSqlRepository: TextToSqlRepository):
        self.query_adapter = query_adapter
        self.llm_client = llm_client
        self.repository = TextToSqlRepository

    async def chat(self, user_input: str, schema_name: str, chat_data: Chat, chat_id: Optional[str]) -> Dict:
        print(chat_data, type(chat_data))
        if not chat_id: 
            chat_id = await self.repository.create_chat(chat_data)
            if not chat_id:
                return None
        try:
            message = Message(role = 1, message= user_input)
            saved_user_message = await self.repository.add_message(chat_id, message)

            if not saved_user_message:
                return {"error": "user message not saved into the database."}
            
            db_structure = self.query_adapter.get_db_structure(schema_name=schema_name)
            print("hola")
            print(db_structure)
            sql_query = self.llm_client.get_model_response(
                db_structure, user_input, schema_name)
            sql_results = self.query_adapter.execute_query(sql_query, schema_name)
            human_response = self.llm_client.get_human_response(user_input)

            saved_bot_message = Message(role = 0, message=sql_results)

            if not saved_bot_message:
                return {"error": "bot message not saved into the database."}
            
            response = {
                "header": human_response,
                "sql_query": sql_query,
                "sql_results": json.dumps(sql_results)
            }
            return response
        except Exception as e:
            return {"error": str(e)}
        

    def get_response(self, user_input: str, schema_name: str):
        try:
            db_structure = self.query_adapter.get_db_structure(schema_name=schema_name)
            sql_query = self.llm_client.get_model_response(
                db_structure, user_input, schema_name)
            return sql_query
        except Exception as e:
            return {"error": str(e)}
        
