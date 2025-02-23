from .config import load_config
import requests
from .prompts import GENERATE_SYNTHETIC_DATA_PROMPT

config = load_config()

class SyntheticDataModelService:
    def __init__(self):
        self.api_key = config['SYNTHETIC_DATA_MODEL_API_KEY']
        self.base_url = config['SYNTHETIC_DATA_BASE_URL']
        self.model = config['SYNTHETIC_DATA_MODEL']
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

        response = requests.post(f"{self.base_url}/chat/completions", headers=headers, json=payload)

        if response.status_code == 200:
            message = response.json()["choices"][0]["message"]["content"]
            self.conversation_history.append({"role": "assistant", "content": message})

            return message
        
        return "Error"
    
    def generate_synthetic_data(self, table_attributes: dict, relations: list, iteratios: int) -> str:
        sql_result = ""
    
        while iterations:
            message = GENERATE_SYNTHETIC_DATA_PROMPT.format(table_attributes = table_attributes, relations = relations)
            response = self.get_model_response(message)

            sql_result += response.replace("```sql", "").replace("```", "").strip()

            print(f"🤖 AI: {response}")

            iterations = iterations - 1

        return sql_result