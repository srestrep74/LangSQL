import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    DB_URL: str = os.getenv('DB_URL')
    TEXTTOSQL_API_KEY: str = os.getenv('TEXTTOSQL_API_KEY')
    TEXTTOSQL_BASE_URL: str = os.getenv('TEXTTOSQL_BASE_URL')
    TEXTTOSQL_MODEL_NAME: str = os.getenv('TEXTTOSQL_MODEL_NAME')
    TEXTTOSQL_TEMPERATURE: str = os.getenv('TEXTTOSQL_TEMPERATURE')
    BASE_URL: str = os.getenv('BASE_URL')
    SYNTHETIC_DATA_MODEL_API_KEY: str = os.getenv(
        'SYNTHETIC_DATA_MODEL_API_KEY')
    SYNTHETIC_DATA_BASE_URL: str = os.getenv('SYNTHETIC_DATA_BASE_URL')
    SYNTHETIC_DATA_MODEL: str = os.getenv('SYNTHETIC_DATA_MODEL')
    MONGO_URI: str = os.getenv('MONGO_URI')
    DB_NAME: str = os.getenv('DB_NAME')
    SECRET_KEY: str = os.getenv('SECRET_KEY')
    ALGORITHM: str = os.getenv('ALGORITHM')
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv('REFRESH_TOKEN_EXPIRE_DAYS'))
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
    GMAIL_USERNAME: str = os.getenv('GMAIL_USERNAME')
    GMAIL_APP_PASSWORD: str = os.getenv('GMAIL_APP_PASSWORD')
    API_URL: str = os.getenv('API_URL')
    TEST_USER: str = os.getenv('TEST_USER')
