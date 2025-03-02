import requests
from typing import Dict
from src.adapters.queries.QueryAdapter import QueryAdapter
from src.modules.text_to_sql.utils.LLMClient import LLMClient
from src.config.constants import Settings
from .prompts import GENERATE_SYNTHETIC_DATA_PROMPT


class SyntheticDataModelService:
    def __init__(self, query_adapter: QueryAdapter):
        self.api_key = Settings.SYNTHETIC_DATA_MODEL_API_KEY
        self.base_url = Settings.SYNTHETIC_DATA_BASE_URL
        self.model = Settings.SYNTHETIC_DATA_MODEL
        self.query_adapter = query_adapter
        self.conversation_history = []

    def get_model_response(self, user_input: str) -> str:
        self.conversation_history.append({"role": "user", "content": user_input})

        payload = {
            "model": self.model,
            "messages": self.conversation_history,
            "temperature": 0.7
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        response = requests.post(f"{self.base_url}", headers=headers, json=payload)

        if response.status_code == 200:
            message = response.json()["choices"][0]["message"]["content"]
            self.conversation_history.append({"role": "assistant", "content": message})

            return message
        
        return "Error"
    
    def generate_synthetic_data(self, iterations: int) -> str:
        sql_result = ""
        db_structure = self.query_adapter.get_db_structure()
    
        while iterations:
            message = GENERATE_SYNTHETIC_DATA_PROMPT.format(db_structure=db_structure)
            response = self.get_model_response(message)

            sql_result += response.replace("```sql", "").replace("```", "").strip()

            iterations = iterations - 1
    
        self.query_adapter.execute_query(sql_result)

        return sql_result


class LangToSqlService:
    def __init__(self, query_adapter: QueryAdapter, llm_client: LLMClient):
        self.query_adapter = query_adapter
        self.llm_client = llm_client

    def process_user_query(self, user_input: str) -> Dict:
        db_structure = self.query_adapter.get_db_structure()
        sql_query = self.llm_client.generate_sql_query(db_structure, user_input)
        sql_results = self.query_adapter.execute_query(sql_query)
        # Here must be a call to llm_client.generate_response(sql_results)
        return sql_results
