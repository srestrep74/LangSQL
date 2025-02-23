from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from .config import load_config
from .prompts import AI_INPUT_PROMPT
from src.modules.queries.service import QueryService
from typing import Dict

config = load_config()

class LangToSqlService:
    def __init__(self, connection_string: str):
        self.api_key = config['TEXTTOSQL_API_KEY']
        self.base_url = config['TEXTTOSQL_BASE_URL']
        self.model = config['TEXTTOSQL_MODEL_NAME']
        self.query_service = QueryService(connection_string)
        self.llm = self.connect()
    
    def connect(self) -> ChatOpenAI:
        return ChatOpenAI(
            model_name = self.model,
            base_url = self.base_url,
            api_key = self.api_key,
            temperature = 0.7
        )
    
    def get_ai_sql(self, user_input: str) -> str:
        db_structure = self.query_service.get_db_structure()
        message = AI_INPUT_PROMPT.format(db_structure = db_structure, user_input = user_input)

        try:
            llm_response = self.llm.invoke([HumanMessage(content=message)])
            return llm_response.content
        except Exception as e:
            return "Response error"
    
    def process_user_query(self, user_input: str) -> Dict:
        sql_query = self.get_ai_sql(user_input)
        print("sql_query", sql_query)
        return self.query_service.execute_query(sql_query)
    
    def conversation(self) -> Dict:
        print("...")
        
        while True: 
            user_input = input("Enter the message: ")
            if user_input.lower() in ["exit", "quit"]:
                print("out")
                break
            sql_query = self.process_user_query(user_input)
            print(f"Sql generado: {sql_query}\n")
