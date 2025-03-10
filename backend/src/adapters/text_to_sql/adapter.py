from typing import Any, Dict, List

from src.modules.text_to_sql.service import LangToSqlService


class TextToSQLAdapter:
    def __init__(self, lang_to_sql_service: LangToSqlService):
        self.lang_to_sql_service = lang_to_sql_service

    def process_user_query(self, user_input: str, schema_name: str) -> Dict:
        return self.lang_to_sql_service.process_user_query(user_input, schema_name)
