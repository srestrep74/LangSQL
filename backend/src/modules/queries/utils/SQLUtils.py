import re

class SQLUtils:
    @staticmethod
    def clean_sql_query(query: str) -> str:
        return re.sub(r'```[a-zA-Z]*', '', query).strip()