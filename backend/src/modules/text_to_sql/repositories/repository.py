from typing import Optional
from bson import ObjectId
from datetime import datetime, UTC

from src.config.database import database
from src.modules.text_to_sql.models.models import Message, Chat


class TextToSqlRepository:
    def __init__(self):
        self.collection = database["Chats"]

    async def create_chat(self, chat_data: Chat) -> Chat:
        try:
            chat_data = chat_data.dict()
            results = await self.collection.insert_one(chat_data)
            print(chat_data, "chat data")
            return str(results.inserted_id)
        except Exception as e:
            print(f"Error creating chat: {e}")
            return None
        
    async def add_message(self, chat_id: str, message: dict) -> Message:
        try:
            
            update_result = await self.collection.update_one(
                {"_id": ObjectId(chat_id)},
                {"$push": {"messages": message}}
            )

            if update_result.modified_count == 1:
                return Message(**message)
        except Exception as e:
            print(f"Error adding message: {e}")
            return None

        
    async def get_chat(self, chat_id: str) -> Chat:
        try:
            result = await self.collection.find_one({"_id": ObjectId(chat_id)})
            if result:
                result["id"] = str(result["_id"])
                del result["_id"]
                return Chat(**result)
            return None
        except Exception:
            return None