
from dotenv import load_dotenv
import os

def load_config():
    load_dotenv(".env")

    config = {
        'SYNTHETIC_DATA_MODEL_API_KEY': os.getenv('SYNTHETIC_DATA_MODEL_API_KEY'),
        'SYNTHETIC_DATA_BASE_URL': os.getenv('SYNTHETIC_DATA_BASE_URL'),
        'SYNTHETIC_DATA_MODEL': os.getenv('SYNTHETIC_DATA_MODEL')
    }

    return config