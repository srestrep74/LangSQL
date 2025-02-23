from src.modules.text_to_sql.config import load_config
from src.modules.text_to_sql.prompts import AI_INPUT_PROMPT
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

class LLMClient:
    def __init__(self):
        config = load_config()
        self.api_key = config['TEXTTOSQL_API_KEY']
        self.base_url = config['TEXTTOSQL_BASE_URL']
        self.model_name = config['TEXTTOSQL_MODEL_NAME']
        self.llm = self._connect()
    
    def _connect(self) -> ChatOpenAI:
        return ChatOpenAI(
            model_name = self.model_name,
            base_url = self.base_url,
            api_key = self.api_key,
            temperature = 0.7
        )

    def generate_sql_query(self, db_structure: str, user_input: str) -> str:
        message = AI_INPUT_PROMPT.format(db_structure = db_structure, user_input = user_input)
        try :
            llm_response = self.llm.invoke([HumanMessage(content=message)])
            return llm_response.content
        except Exception as e:
            return "Response error"