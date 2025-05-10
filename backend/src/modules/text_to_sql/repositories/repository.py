from bson import ObjectId
from typing import List
from src.config.database import database
from src.modules.text_to_sql.models.models import Message, Chat


class TextToSqlRepository:
    def __init__(self):
        self.collection = database["Chats"]

    async def create_chat(self, chat_data: Chat) -> str:
        try:
            chat_data = chat_data.dict()
            results = await self.collection.insert_one(chat_data)
            return str(results.inserted_id)
        except Exception as e:
            print(f"Error creating chat: {e}")
            return None

    async def add_message(self, chat_id: str, message: Message) -> bool:
        try:
            message = message.dict()
            update_result = await self.collection.update_one(
                {"_id": ObjectId(chat_id)},
                {"$push": {"messages": message}}
            )

            if update_result.modified_count == 1:
                return True
        except Exception as e:
            print(f"Error adding message: {e}")
            return False

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
    
    async def get_users_chats(self, user_id: str) -> List[Chat]:
        try:
            chats = []
            async for chat in self.collection.find({"user_id": user_id}):
                chat["id"] = str(chat["_id"])
                del chat["_id"]
                chats.append(
                    {
                        "chat_id": chat["id"],
                        "title": chat.get("title", "Untitled Chat")
                    }
                )
            return chats
        except Exception:
            return []
    
    async def delete_chat(self, chat_id: str) -> bool:
        """
        Delete a chat from the database by its ID.
        
        Args:
            chat_id (str): The ID of the chat to delete
            
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        try:
            delete_result = await self.collection.delete_one({"_id": ObjectId(chat_id)})
            return delete_result.deleted_count == 1
        except Exception as e:
            print(f"Error deleting chat: {e}")
            return False
    
    async def update_chat_title(self, chat_id: str, new_title: str) -> bool:
        """
        Update the title of a chat.
        
        Args:
            chat_id (str): The ID of the chat to update
            new_title (str): The new title for the chat
            
        Returns:
            bool: True if update was successful, False otherwise
        """
        try:
            update_result = await self.collection.update_one(
                {"_id": ObjectId(chat_id)},
                {"$set": {"title": new_title}}
            )
            return update_result.modified_count == 1
        except Exception as e:
            print(f"Error updating chat title: {e}")
            return False