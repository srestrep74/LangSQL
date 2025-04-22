
from src.modules.queries.schemas.DatabaseConnection import DatabaseConnection
from src.modules.text_to_sql.service import LangToSqlService


class TextToSQLAdapter:
    def __init__(self, lang_to_sql_service: LangToSqlService):
        self.lang_to_sql_service = lang_to_sql_service

    def get_response(self, user_input: str, connection: DatabaseConnection) -> str:
        return self.lang_to_sql_service.get_response(user_input, connection)
