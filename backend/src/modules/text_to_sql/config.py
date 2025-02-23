from dotenv import load_dotenv
import os

def load_config():
    load_dotenv(".env")
    config = {
        'TEXTTOSQL_API_KEY': os.getenv('TEXTTOSQL_API_KEY'),
        'TEXTTOSQL_BASE_URL': os.getenv('TEXTTOSQL_BASE_URL'),
        'TEXTTOSQL_MODEL_NAME': os.getenv('TEXTTOSQL_MODEL_NAME')
    }
    return config
