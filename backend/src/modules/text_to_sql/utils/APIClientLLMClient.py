import requests
from src.config.constants import Settings
from src.modules.text_to_sql.utils.ILLMCLient import ILLMClient

class APIClientLLMClient(ILLMClient):
    def __init__(self):
        self.api_key = Settings.SYNTHETIC_DATA_MODEL_API_KEY
        self.base_url = Settings.SYNTHETIC_DATA_BASE_URL
        self.model = Settings.SYNTHETIC_DATA_MODEL
        self.conversation_history = []

    def get_model_response(self, db_structure: str, user_input: str) -> str:
        
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
        print(response.json())

        if response.status_code == 200:
            message = response.json()["choices"][0]["message"]["content"]
            self.conversation_history.append({"role": "assistant", "content": message})
            return message
        return "Error"
