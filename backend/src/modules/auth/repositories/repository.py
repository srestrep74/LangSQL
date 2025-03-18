from bson import ObjectId
from typing import Optional
from src.config.database import database
from src.modules.auth.models.models import UserPatch, UserCreate, User


class UserRepository:
    def __init__(self):
        self.collection = database["Users"]

    async def create_user(self, user_data: UserCreate) -> User:
        user_dict = user_data.model_dump()
        result = await self.collection.insert_one(user_dict)
        user_dict["id"] = str(result.inserted_id)
        return User(**user_dict)

    async def get_by_id(self, user_id: str) -> Optional[User]:
        try:
            result = await self.collection.find_one({"_id": ObjectId(user_id)})
            if result:
                result["id"] = str(result["_id"])
                del result["_id"]
                return User(**result)
            return None
        except Exception:
            return None

    async def update_user(self, user_id: str, user_data: UserPatch) -> Optional[User]:
        # Filter out None values to only update provided fields
        update_data = {k: v for k, v in user_data.model_dump().items() if v is not None}
        
        if not update_data:
            return await self.get_by_id(user_id)
        
        try:
            result = await self.collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": update_data}
            )
            
            if result.matched_count:
                return await self.get_by_id(user_id)
            return None
        except Exception:
            return None

    async def delete_user(self, user_id: str) -> bool:
        try:
            result = await self.collection.delete_one({"_id": ObjectId(user_id)})
            return result.deleted_count > 0
        except Exception:
            return False