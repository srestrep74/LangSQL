from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

from src.config.constants import Settings
from src.modules.text_to_sql.prompts.lang_to_sql import (
    AI_INPUT_PROMPT,
    HUMAN_RESPONSE_PROMPT,
)
from src.modules.text_to_sql.utils.ILLMCLient import ILLMClient


class LangChainLLMClient(ILLMClient):
    def __init__(self):
        self.api_key = Settings.TEXTTOSQL_API_KEY
        self.base_url = Settings.TEXTTOSQL_BASE_URL
        self.model_name = Settings.TEXTTOSQL_MODEL_NAME
        self.MODEL_TEMPERATURE = Settings.TEXTTOSQL_TEMPERATURE
        self.llm = self._connect()

    def _connect(self) -> ChatOpenAI:
        return ChatOpenAI(
            model_name=self.model_name,
            base_url=self.base_url,
            api_key=self.api_key,
            temperature=self.MODEL_TEMPERATURE
        )

    def get_model_response(self, db_structure: str, user_input: str, schema_name) -> str:
        message = AI_INPUT_PROMPT.format(
            db_structure=db_structure, user_input=user_input, schema_name=schema_name
        )
        try:
            llm_response = self.llm.invoke([HumanMessage(content=message)])
            return llm_response.content
        except Exception as e:
            return e

    def get_human_response(self, question: str) -> str:
        message = HUMAN_RESPONSE_PROMPT.format(
            human_question=question
        )
        try:
            llm_response = self.llm.invoke([HumanMessage(content=message)])
            return llm_response.content
        except Exception as e:
            return e
