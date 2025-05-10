import json
from typing import Dict, List, Optional

from src.adapters.queries.QueryAdapter import QueryAdapter
from src.modules.queries.utils.SQLUtils import SQLUtils
from src.modules.text_to_sql.prompts.synthetic_data import (
    GENERATE_SYNTHETIC_DATA_PROMPT,
)
from src.modules.text_to_sql.utils.ILLMCLient import ILLMClient
from src.modules.queries.schemas.DatabaseConnection import DatabaseConnection
from src.modules.text_to_sql.models.models import Chat, Message
from src.modules.text_to_sql.repositories.repository import TextToSqlRepository


class SyntheticDataModelService:
    def __init__(self, query_adapter: QueryAdapter, llm_client: ILLMClient):
        self.query_adapter = query_adapter
        self.llm_client = llm_client

    def generate_synthetic_data(self, iterations: int, connection: DatabaseConnection) -> str:
        iterations = iterations // 40
        print(f"Generando datos sintéticos para {iterations} iteraciones...")
        db_structure = self.query_adapter.get_db_structure(connection)
        user_input = GENERATE_SYNTHETIC_DATA_PROMPT.format(
            db_structure=db_structure, schema_name=connection.schema_name)
        last_query = ""

        for _ in range(iterations):
            try:
                print(f"Generando datos sintéticos para la iteración {_ + 1}...")
                last_query = self.llm_client.get_model_response(user_input)
                print("LlM response:", last_query)
                last_query = SQLUtils.clean_sql_query(last_query)
                print("Insertando datos sintéticos...")
                self.query_adapter.execute_query(last_query, connection)
                print("Datos sintéticos insertados correctamente.")
            except Exception as e:
                return {"error": str(e)}
        return last_query


class LangToSqlService:
    def __init__(self, query_adapter: QueryAdapter, llm_client: ILLMClient, TextToSqlRepository: TextToSqlRepository):
        self.query_adapter = query_adapter
        self.llm_client = llm_client
        self.repository = TextToSqlRepository

    async def chat(self, connection: DatabaseConnection, user_input: Optional[str], chat_data: Chat, chat_id: str) -> Dict:
        if chat_id:
            existing_chat = await self.repository.get_chat(chat_id)
            if not existing_chat:
                chat_id = await self.repository.create_chat(chat_data)
                if not chat_id:
                    return {"error": "Failed to create chat"}
        elif not chat_id:
            chat_id = await self.repository.create_chat(chat_data)
            if not chat_id:
                return {"error": "Failed to create chat"}
        
        if not user_input:
            chats = await self.get_chats(chat_data.user_id)
            full_chat = await self.get_messages(chat_id)
            response = {
                "chat_id": chat_id,
                "header": "Chat",
                "sql_query": "",
                "sql_results": [],
                "chats": chats,
                "messages": full_chat["messages"]
            }
            return response
        try:
            user_message = Message(role=1, message=user_input)
            saved_user_message = await self.repository.add_message(chat_id, user_message)

            if not saved_user_message:
                return {"error": "user message not saved into the database."}

            db_structure = self.query_adapter.get_db_structure(connection)
            db_type = connection.db_type
            chat_history = await self.get_messages(chat_id)
            sql_query = self.llm_client.get_model_response(
                db_structure, user_input, connection.schema_name, chat_history, db_type)
            sql_results = self.query_adapter.execute_query(sql_query, connection)
            human_response = self.llm_client.get_human_response(user_input)
            bot_message = Message(role=0, message=human_response + '\n' + str(sql_results))
            saved_bot_message = await self.repository.add_message(chat_id, bot_message)

            if not saved_bot_message:
                return {"error": "bot message not saved into the database."}

            chats = await self.get_chats(chat_data.user_id)
            full_chat = await self.get_messages(chat_id)

            response = {
                "chat_id": chat_id,
                "header": human_response,
                "sql_query": sql_query,
                "sql_results": json.dumps(sql_results),
                "chats": chats,
                "messages": full_chat["messages"]
            }
            return response
        except Exception as e:
            return {"error": str(e)}

    async def get_messages(self, chat_id: str) -> Dict:
        response = await self.repository.get_chat(chat_id)
        if response is None:
            return {"messages": []}
        
        messages = response.messages
        return {
            "messages": messages
        }

    def get_response(self, user_input: str, connection: DatabaseConnection):
        try:
            db_structure = self.query_adapter.get_db_structure(connection)
            sql_query = self.llm_client.get_model_response(
                db_structure, user_input, connection.schema_name)
            return sql_query
        except Exception as e:
            return {"error": str(e)}
    
    async def get_chats(self, user_id: str) -> List[Dict]:
        try:
            return await self.repository.get_users_chats(user_id)
        except Exception as e:
            print(f"Error getting chats for user {user_id}: {str(e)}")
            return []
