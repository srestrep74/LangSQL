import google.generativeai as genai

from src.config.constants import Settings
from src.modules.text_to_sql.utils.ILLMCLient import ILLMClient


class APIClientLLMClient(ILLMClient):
    def __init__(self):
        self.api_key = Settings.SYNTHETIC_DATA_MODEL_API_KEY
        self.base_url = Settings.SYNTHETIC_DATA_BASE_URL
        self.model_name = Settings.SYNTHETIC_DATA_MODEL
        self.conversation_history = []
        self.MODEL_TEMPERATURE = 0.7

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config={
                "temperature": self.MODEL_TEMPERATURE
            }
        )

    def _post_request(self) -> dict:
        try:
            response = self.model.generate_content(self.conversation_history)
            self.conversation_history.append({"role": "assistant", "parts": [response.text]})
            return response.text
        except Exception as e:
            return {"error": str(e)}

    def get_model_response(self, user_input: str) -> str:
        self.conversation_history.append({"role": "user", "parts": [user_input]})

        response = self._post_request()
        return response
