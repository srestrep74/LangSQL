from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Dict

from src.config.constants import Settings
from src.modules.reports.prompts.additional_info import (
    ADDITIONAL_INFO_PROMPT, TRANSLATE_PROMPT
)


class AdditionalInfoClient:
    def __init__(self):
        self.api_key = Settings.TEXTTOSQL_API_KEY
        self.base_url = Settings.TEXTTOSQL_BASE_URL
        self.model_name = Settings.TEXTTOSQL_MODEL_NAME
        self.MODEL_TEMPERATURE = Settings.TEXTTOSQL_TEMPERATURE
        self.llm = self._connect()

    def _connect(self) -> ChatGoogleGenerativeAI:
        return ChatGoogleGenerativeAI(
            model=self.model_name,
            google_api_key=self.api_key,
            temperature=self.MODEL_TEMPERATURE,
            max_output_tokens=200,
            stop=[";"]
        )

    def get_additional_info(self, graph: Dict[str, dict]) -> str:
        message = ADDITIONAL_INFO_PROMPT.format(
            graph=graph
        )
        try:
            llm_response = self.llm.invoke([HumanMessage(content=message)])
            return llm_response.content
        except Exception as e:
            return e

    def translate(self, text: str) -> str:
        message = TRANSLATE_PROMPT.format(
            text=text
        )
        try:
            llm_response = self.llm.invoke([HumanMessage(content=message)])
            return llm_response.content
        except Exception as e:
            return e
