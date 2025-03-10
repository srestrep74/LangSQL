from motor.motor_asyncio import AsyncIOMotorClient
from src.config.constants import Settings

MONGO_URI = Settings.MONGO_URI
DB_NAME = Settings.DB_NAME

client = AsyncIOMotorClient(MONGO_URI)
database = client[DB_NAME]