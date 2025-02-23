from src.adapters.queries.QueryAdapter import QueryAdapter
from typing import Dict

from src.modules.text_to_sql.utils.LLMClient import LLMClient

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
    
    # This method only for debugging
    def conversation(self) -> Dict:
        while True: 
            user_input = input("Enter the message: ")
            if user_input.lower() in ["exit", "quit"]:
                print("out")
                break
            results = self.process_user_query(user_input)
            print(f"Results: {results}\n")
