from typing import Any, Dict, Optional

from bson import ObjectId

from src.modules.auth.models.models import User, UserCreate, UserPatch
from src.modules.auth.repositories.repository import UserRepository

from src.modules.auth.utils.util import hash_password, verify_password, create_tokens
from src.config.constants import Settings
from datetime import timedelta


class UserService:
    def __init__(self):
        self.repository = UserRepository()

    async def create_user(self, user_data: UserCreate) -> User:
        hashed_password = hash_password(user_data.password)
        user_data.password = hashed_password
        return await self.repository.create_user(user_data)

    async def get_user(self, user_id: str) -> User:
        return await self.repository.get_by_id(user_id)

    async def update_user(self, user_id: str, user_data: UserPatch) -> User:
        return await self.repository.update_user(user_id, user_data)

    async def delete_user(self, user_id: str) -> bool:
        return await self.repository.delete_user(user_id)

    async def login(self, email: str, password: str) -> Optional[User]:
        user = await self.repository.collection.find_one({"email": email})

        if user and verify_password(password, user["password"]):
            access_token, refresh_token = create_tokens(
                data={
                    "sub": user["email"]
                }
            )

            user["id"] = str(user["_id"])
            user.pop("_id", None)
            user.pop("password", None)

            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
                "user": user
            }
        return None

    # Methods for queries list
    async def add_query(self, user_id: str, query_id: str) -> Optional[User]:
        """
        Add a query ID to user's queries list.

        Args:
            user_id: ID of the user
            query_id: ID of the query to add

        Returns:
            Updated User if successful, None otherwise
        """
        try:
            result = await self.repository.collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$addToSet": {"queries": query_id}}  # $addToSet prevents duplicates
            )

            if result.modified_count > 0 or result.matched_count > 0:
                return await self.get_user(user_id)
            return None
        except Exception:
            return None

    async def remove_query(self, user_id: str, query_id: str) -> Optional[User]:
        """
        Remove a query ID from user's queries list.

        Args:
            user_id: ID of the user
            query_id: ID of the query to remove

        Returns:
            Updated User if successful, None otherwise
        """
        try:
            result = await self.repository.collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$pull": {"queries": query_id}}
            )

            if result.modified_count > 0 or result.matched_count > 0:
                return await self.get_user(user_id)
            return None
        except Exception:
            return None

    # Methods for alerts list

    async def add_alert(self, user_id: str, alert_id: str) -> Optional[User]:
        """
        Add an alert ID to user's alerts list.

        Args:
            user_id: ID of the user
            alert_id: ID of the alert to add

        Returns:
            Updated User if successful, None otherwise
        """
        try:
            result = await self.repository.collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$addToSet": {"alerts": alert_id}}  # $addToSet prevents duplicates
            )

            if result.modified_count > 0 or result.matched_count > 0:
                return await self.get_user(user_id)
            return None
        except Exception:
            return None

    async def remove_alert(self, user_id: str, alert_id: str) -> Optional[User]:
        """
        Remove an alert ID from user's alerts list.

        Args:
            user_id: ID of the user
            alert_id: ID of the alert to remove

        Returns:
            Updated User if successful, None otherwise
        """
        try:
            result = await self.repository.collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$pull": {"alerts": alert_id}}
            )

            if result.modified_count > 0 or result.matched_count > 0:
                return await self.get_user(user_id)
            return None
        except Exception:
            return None

    # Credentials management methods

    async def add_credential(self, user_id: str, credential: Dict[str, Any]) -> Optional[User]:
        """
        Add a new credential to user's credentials list.

        Args:
            user_id: ID of the user
            credential: Dict[str, Any] object with database connection information

        Returns:
            Updated User if successful, None otherwise
        """
        try:
            result = await self.repository.collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$addToSet": {"credentials": credential}}
            )

            if result.modified_count > 0 or result.matched_count > 0:
                return await self.get_user(user_id)
            return None
        except Exception as e:
            print(f"Error adding credential: {e}")
            return None

    async def remove_credential(self, user_id: str, credential_index: int) -> Optional[User]:
        """
        Remove a credential from user's credentials list by index.

        Args:
            user_id: ID of the user
            credential_index: Index of the credential to remove

        Returns:
            Updated User if successful, None otherwise
        """
        try:
            # First get the user to check if index is valid and not the main credential
            user = await self.get_user(user_id)
            if not user or credential_index < 0 or credential_index >= len(user.credentials):
                return None

            # Get the credential to remove
            credential_to_remove = user.credentials[credential_index]

            # Check if this is the main credential
            if user.main_credentials == credential_to_remove:
                # Cannot remove the main credential
                return None

            # Remove the credential at the specified index
            result = await self.repository.collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$pull": {"credentials": credential_to_remove}}
            )

            if result.modified_count > 0:
                return await self.get_user(user_id)
            return None
        except Exception as e:
            print(f"Error removing credential: {e}")
            return None

    async def set_main_credential(self, user_id: str, credential_index: int) -> Optional[User]:
        """
        Set a credential from the credentials list as the main credential.

        Args:
            user_id: ID of the user
            credential_index: Index of the credential to set as main

        Returns:
            Updated User if successful, None otherwise
        """
        try:
            # First get the user to check if index is valid
            user = await self.get_user(user_id)
            if not user or credential_index < 0 or credential_index >= len(user.credentials):
                return None

            # Get the credential to set as main
            new_main_credential = user.credentials[credential_index]

            # Update the main credential
            result = await self.repository.collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"main_credentials": new_main_credential}}
            )

            if result.modified_count > 0 or result.matched_count > 0:
                return await self.get_user(user_id)
            return None
        except Exception as e:
            print(f"Error setting main credential: {e}")
            return None
