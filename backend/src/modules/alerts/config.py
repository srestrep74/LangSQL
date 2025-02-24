from dotenv import load_dotenv
import os

def load_config():
    load_dotenv(".env")
    
    config = {
        "MONGO_URI": os.getenv("MONGO_URI"),
        "DB_NAME": os.getenv("DB_NAME"),
    }

    return config