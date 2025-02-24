from motor.motor_asyncio import AsyncIOMotorClient
from .config import load_config

config = load_config()

MONGO_URI = config["MONGO_URI"]
DB_NAME = config["DB_NAME"]

client = AsyncIOMotorClient(MONGO_URI)
database = client[DB_NAME]