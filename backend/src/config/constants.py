from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    DB_URL: str = os.getenv('DB_URL')
    TEXTTOSQL_API_KEY: str = os.getenv('TEXTTOSQL_API_KEY')
    TEXTTOSQL_BASE_URL: str = os.getenv('TEXTTOSQL_BASE_URL')
    TEXTTOSQL_MODEL_NAME: str = os.getenv('TEXTTOSQL_MODEL_NAME')
    BASE_URL: str = os.getenv('BASE_URL')
