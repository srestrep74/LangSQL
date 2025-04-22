from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from bson import ObjectId

from src.modules.auth.models.models import UserPatch
from src.modules.auth.service import UserService


class TestUserService:
    @pytest.fixture
    def user_service(self):
        return UserService()

    @pytest.fixture
    def mock_user_data(self):
        return {
            "_id": ObjectId("507f1f77bcf86cd799439011"),
            "email": "test@example.com",
            "password": "hashed_password",
            "queries": [],
            "alerts": [],
            "credentials": [],
            "main_credentials": None
        }

    @pytest.fixture
    def mock_credential(self):
        return {
            "db_type": "postgresql",
            "host": "localhost",
            "username": "user",
            "password": "pass",
            "database_name": "test_db"
        }

    @pytest.mark.asyncio
    async def test_get_user(self, user_service, mock_user_data):
        user_id = "507f1f77bcf86cd799439011"

        with patch.object(user_service.repository, 'get_by_id', AsyncMock(return_value=mock_user_data)) as mock_get:
            result = await user_service.get_user(user_id)

            mock_get.assert_called_once_with(user_id)
            assert result == mock_user_data

    @pytest.mark.asyncio
    async def test_update_user(self, user_service, mock_user_data):
        user_id = "507f1f77bcf86cd799439011"
        user_data = UserPatch(full_name="Updated Name")

        with patch.object(user_service.repository, 'update_user', AsyncMock(return_value=mock_user_data)) as mock_update:
            result = await user_service.update_user(user_id, user_data)

            mock_update.assert_called_once_with(user_id, user_data)
            assert result == mock_user_data

    @pytest.mark.asyncio
    async def test_delete_user(self, user_service):
        user_id = "507f1f77bcf86cd799439011"

        with patch.object(user_service.repository, 'delete_user', AsyncMock(return_value=True)) as mock_delete:
            result = await user_service.delete_user(user_id)

            mock_delete.assert_called_once_with(user_id)
            assert result is True

    @pytest.mark.asyncio
    async def test_login_success(self, user_service, mock_user_data):
        email = "test@example.com"
        password = "correct_password"

        mock_user_data["password"] = "hashed_password"

        with patch.object(user_service.repository.collection, 'find_one', AsyncMock(return_value=mock_user_data)), \
                patch('src.modules.auth.service.verify_password', MagicMock(return_value=True)), \
                patch('src.modules.auth.service.create_tokens', MagicMock(return_value=("access_token", "refresh_token"))):

            result = await user_service.login(email, password)

            assert result is not None
            assert "access_token" in result
            assert "refresh_token" in result
            assert "user" in result
            assert "password" not in result["user"]

    @pytest.mark.asyncio
    async def test_login_failure(self, user_service):
        email = "test@example.com"
        password = "wrong_password"

        with patch.object(user_service.repository.collection, 'find_one', AsyncMock(return_value=None)):
            result = await user_service.login(email, password)
            assert result is None

    @pytest.mark.asyncio
    async def test_add_credential_success(self, user_service, mock_user_data, mock_credential):
        user_id = "507f1f77bcf86cd799439011"

        with patch.object(user_service.repository.collection, 'update_one', AsyncMock(return_value=MagicMock(modified_count=1))), \
                patch.object(user_service, 'get_user', AsyncMock(return_value=mock_user_data)):

            result = await user_service.add_credential(user_id, mock_credential)

            assert result == mock_user_data

    @pytest.mark.asyncio
    async def test_add_credential_failure(self, user_service, mock_credential):
        user_id = "507f1f77bcf86cd799439011"

        with patch.object(user_service.repository.collection, 'update_one', AsyncMock(side_effect=Exception("DB Error"))):
            result = await user_service.add_credential(user_id, mock_credential)

            assert result is None

    @pytest.mark.asyncio
    async def test_remove_credential_invalid_index(self, user_service, mock_user_data):
        user_id = "507f1f77bcf86cd799439011"
        credential_index = 999  # Invalid index

        with patch.object(user_service, 'get_user', AsyncMock(return_value=mock_user_data)):
            result = await user_service.remove_credential(user_id, credential_index)

            assert result is None

    @pytest.mark.asyncio
    async def test_remove_main_credential(self, user_service, mock_user_data, mock_credential):
        user_id = "507f1f77bcf86cd799439011"
        credential_index = 0

        # Set up mock user with main credential
        mock_user_data["credentials"] = [mock_credential]
        mock_user_data["main_credentials"] = mock_credential

        with patch.object(user_service, 'get_user', AsyncMock(return_value=mock_user_data)):
            result = await user_service.remove_credential(user_id, credential_index)

            assert result is None

    @pytest.mark.asyncio
    async def test_set_main_credential_invalid_index(self, user_service, mock_user_data):
        user_id = "507f1f77bcf86cd799439011"
        credential_index = 999  # Invalid index

        with patch.object(user_service, 'get_user', AsyncMock(return_value=mock_user_data)):
            result = await user_service.set_main_credential(user_id, credential_index)

            assert result is None
