from typing import Optional

from fastapi import APIRouter, Body, Depends, status

from src.config.dependencies import (
    get_lang_to_sql_service,
    get_synthetic_data_model_service,
)
from src.modules.queries.schemas.DatabaseConnection import DatabaseConnection
from src.modules.text_to_sql.models.models import Chat
from src.modules.text_to_sql.service import LangToSqlService, SyntheticDataModelService
from src.utils.ResponseManager import ResponseManager

router = APIRouter()


@router.post("/chat")
async def chat(
    connection: DatabaseConnection,
    user_input: Optional[str] = Body(None, embed=True),
    chat_data: Chat = Body(..., embed=True),
    chat_id: Optional[str] = Body(None, embed=True),
    lang_to_sql_service: LangToSqlService = Depends(get_lang_to_sql_service)
):
    """
    This endpoint processes a user query and converts it into an SQL statement.

    Args:
        connection (DatabaseConnection): The database connection details including type, credentials, host, port, and schema.
        user_input (str): The user's query that needs to be converted into SQL.
        chat_data (Chat): Chat-related information, including user ID and previous messages.
        chat_id (Optional[str]): The identifier for an existing chat. If None, a new chat will be created.
        lang_to_sql_service (LangToSqlService): A service for processing user queries into SQL, injected via `Depends(get_lang_to_sql_service)`.

    Returns:
        Successful Response (`200 OK`)
        ```json
        {
            "status": "success",
            "message": "Success",
            "data": {
                "results": "SQL Query String"
            }
        }
        ```

        Error Response (`400 Bad Request`)
        ```json
        {
            "status": "error",
            "message": "Error",
            "details": {
                "error": "Error description"
            }
        }
        ```
    """
    try:
        results = await lang_to_sql_service.chat(connection, user_input, chat_data, chat_id)
        return ResponseManager.success_response(
            data={"results": results},
            message="Success",
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        return ResponseManager.error_response(
            message="Error",
            status_code=status.HTTP_400_BAD_REQUEST,
            details={"error": str(e)},
        )


@router.delete("/chat")
async def delete_chat(
    chat_id: str = Body(..., embed=True),
    user_id: str = Body(..., embed=True),
    connection: DatabaseConnection = Body(..., embed=True),
    lang_to_sql_service: LangToSqlService = Depends(get_lang_to_sql_service)
):
    """
    Endpoint to delete a specific chat.

    Args:
        chat_id (str): The unique identifier for the chat to be deleted.
        user_id (str): The user ID associated with the chat.
        connection (DatabaseConnection): The database connection details.
        lang_to_sql_service (LangToSqlService): Service for chat operations.

    Returns:
        Successful Response (`200 OK`)
        ```json
        {
            "status": "success",
            "message": "Chat deleted successfully",
            "data": {}
        }
        ```

        Error Response (`400 Bad Request`)
        ```json
        {
            "status": "error",
            "message": "Error deleting chat",
            "details": {
                "error": "Error description"
            }
        }
        ```
    """
    try:
        await lang_to_sql_service.delete_chat(chat_id, user_id)

        return ResponseManager.success_response(
            data={},
            message="Chat deleted successfully",
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        return ResponseManager.error_response(
            message="Error deleting chat",
            status_code=status.HTTP_400_BAD_REQUEST,
            details={"error": str(e)},
        )


@router.put("/chat/rename")
async def rename_chat(
    chat_id: str = Body(..., embed=True),
    user_id: str = Body(..., embed=True),
    new_title: str = Body(..., embed=True),
    connection: DatabaseConnection = Body(..., embed=True),
    lang_to_sql_service: LangToSqlService = Depends(get_lang_to_sql_service)
):
    """
    Endpoint to rename a specific chat.

    Args:
        chat_id (str): The unique identifier for the chat to be renamed.
        user_id (str): The user ID associated with the chat.
        new_title (str): The new title for the chat.
        connection (DatabaseConnection): The database connection details.
        lang_to_sql_service (LangToSqlService): Service for chat operations.

    Returns:
        Successful Response (`200 OK`)
        ```json
        {
            "status": "success",
            "message": "Chat renamed successfully",
            "data": {}
        }
        ```

        Error Response (`400 Bad Request`)
        ```json
        {
            "status": "error",
            "message": "Error renaming chat",
            "details": {
                "error": "Error description"
            }
        }
        ```
    """
    try:
        await lang_to_sql_service.rename_chat(chat_id, user_id, new_title)

        return ResponseManager.success_response(
            data={},
            message="Chat renamed successfully",
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        return ResponseManager.error_response(
            message="Error renaming chat",
            status_code=status.HTTP_400_BAD_REQUEST,
            details={"error": str(e)},
        )


@router.get("/get_messages")
async def get_messages(
    chat_id: str = Body(..., embed=True),
    lang_to_sql_service: LangToSqlService = Depends(get_lang_to_sql_service)
):
    """
    Endpoint to retrieve messages from an existing chat.

    Args:
        chat_id (str): The unique identifier for the chat from which messages will be retrieved.
        lang_to_sql_service (LangToSqlService): A dependency injected service for managing chat data retrieval.

    Returns:
        Successful Response (`200 OK`)
        ```json
        {
            "status": "success",
            "message": "Success",
            "data": {
                "results": ["Message 1", "Message 2", "..."]
            }
        }
        ```

        Error Response (`400 Bad Request`)
        ```json
        {
            "status": "error",
            "message": "Error retrieving messages",
            "details": {
                "error": "Error description"
            }
        }
        ```
    """
    try:
        results = await lang_to_sql_service.get_messages(chat_id)

        return ResponseManager.success_response(
            data={"results": results},
            message="Success",
            status_code=status.HTTP_200_OK,
        )

    except Exception as e:
        return ResponseManager.error_response(
            message="Error",
            status_code=status.HTTP_400_BAD_REQUEST,
            details={"error": str(e)},
        )


@router.post("/generate_synthetic_data")
async def generate_synthetic_data(
    connection: DatabaseConnection,
    iterations: int = Body(..., embed=True),
    synthetic_data_model_service: SyntheticDataModelService = Depends(get_synthetic_data_model_service)
):
    """
    This endpoint generates synthetic data and inserts it into the user database.

    Args:

        synthetic_data_model_service: A service for generating synthetic data. Retrieved via `Depends(get_synthetic_data_model_service)`.

    Returns:

        Successful Response (`200 OK`)
        ```json
        {
            "status": "success",
            "message": "Success",
            "data": {
                "results": [...]
            }
        }
        ```

        Error Response (`400 Bad Request`)
        ```json
        {
            "status": "error",
            "message": "Error",
            "details": {
                "error": "Error description"
            }
        }
        ```
    """
    try:
        results = await synthetic_data_model_service.generate_synthetic_data(iterations, connection)

        return ResponseManager.success_response(
            data={"results": results},
            message="Success",
            status_code=status.HTTP_200_OK,
        )

    except Exception as e:
        return ResponseManager.error_response(
            message="Error",
            status_code=status.HTTP_400_BAD_REQUEST,
            details={"error": str(e)},
        )


@router.post("/get_chats")
async def get_chats(
    user_id: str = Body(..., embed=True),
    connection: DatabaseConnection = Body(..., embed=True),
    lang_to_sql_service: LangToSqlService = Depends(get_lang_to_sql_service)
):
    """
    Endpoint to retrieve all chats for a user without creating a new chat.

    Args:
        user_id (str): The user ID for which to retrieve chats.
        connection (DatabaseConnection): The database connection details.
        lang_to_sql_service (LangToSqlService): Service for chat operations.

    Returns:
        Successful Response (`200 OK`)
        ```json
        {
            "status": "success",
            "message": "Success",
            "data": {
                "results": {
                    "chats": [{"chat_id": "...", "title": "..."}]
                }
            }
        }
        ```

        Error Response (`400 Bad Request`)
        ```json
        {
            "status": "error",
            "message": "Error retrieving chats",
            "details": {
                "error": "Error description"
            }
        }
        ```
    """
    try:
        chats = await lang_to_sql_service.get_chats(user_id)

        return ResponseManager.success_response(
            data={"results": {"chats": chats}},
            message="Success",
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        return ResponseManager.error_response(
            message="Error retrieving chats",
            status_code=status.HTTP_400_BAD_REQUEST,
            details={"error": str(e)},
        )
