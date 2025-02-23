from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from .config import load_config
from .prompts import AI_INPUT_PROMPT
from typing import Dict

config = load_config()

class LangToSqlService:
    def __init__(self, db_structure: str):
        self.api_key = config['TEXTTOSQL_API_KEY']
        self.base_url = config['TEXTTOSQL_BASE_URL']
        self.model = config['TEXTTOSQL_MODEL_NAME']
        self.db_structure = db_structure
        self.llm = self.connect()
    
    def connect(self) -> ChatOpenAI:
        return ChatOpenAI(
            model_name = self.model,
            base_url = self.base_url,
            api_key = self.api_key,
            temperature = 0.7
        )
    
    def get_ai_sql(self, user_input: str) -> str:
        message = AI_INPUT_PROMPT.format(db_structure = self.db_structure, user_input = user_input)

        try:
            llm_response = self.llm.invoke([HumanMessage(content=message)])
            return llm_response.content
        except Exception as e:
            return "Response error"
    
    def conversation(self) -> Dict:
        print("...")
        
        while True: 
            user_input = input("Enter the message: ")
            if user_input.lower() in ["exit", "quit"]:
                print("out")
                break
            sql_query = self.get_ai_sql(user_input)
            print(f"Sql generado: {sql_query}\n")
