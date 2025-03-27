from typing import Any, Dict

from fastapi import APIRouter, Body, status

from src.modules.auth.models.models import User, UserCreate, UserPatch
from src.modules.auth.service import UserService
from src.utils.ResponseErrorModel import ResponseError
from src.utils.ResponseManager import ResponseManager

router = APIRouter()
service = UserService()


@router.post("/create",
             tags=["User"],
             responses={
                 201: {"model": User, "description": "User created successfully"},
                 500: {"model": ResponseError, "description": "Internal server error."},
             })
async def create_user(user_data: UserCreate):
    """
    Creates a new user in the database.

    Args:
        user_data: UserCreate model with user information

    Returns:
        User: The created user object
    """
    try:
        result = await service.create_user(user_data)
        return ResponseManager.success_response(result, status_code=status.HTTP_201_CREATED)
    except Exception as e:
        return ResponseManager.error_response(str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/{user_id}",
            tags=["User"],
            responses={
                200: {"model": User, "description": "User found"},
                404: {"model": ResponseError, "description": "User not found"},
                500: {"model": ResponseError, "description": "Internal server error."},
            })
async def get_user(user_id: str):
    """
    Gets a user by ID.

    Args:
        user_id: ID of the user to retrieve

    Returns:
        User: The user object if found
    """
    try:
        result = await service.get_user(user_id)
        if not result:
            return ResponseManager.error_response("User not found", status_code=status.HTTP_404_NOT_FOUND)
        return ResponseManager.success_response(result)
    except Exception as e:
        return ResponseManager.error_response(str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.patch("/{user_id}",
              tags=["User"],
              responses={
                  200: {"model": User, "description": "User updated successfully"},
                  404: {"model": ResponseError, "description": "User not found"},
                  500: {"model": ResponseError, "description": "Internal server error."},
              })
async def update_user(user_id: str, user_data: UserPatch):
    """
    Updates a user.

    Args:
        user_id: ID of the user to update
        user_data: UserPatch model with fields to update

    Returns:
        User: The updated user object
    """
    try:
        result = await service.update_user(user_id, user_data)
        if not result:
            return ResponseManager.error_response("User not found", status_code=status.HTTP_404_NOT_FOUND)
        return ResponseManager.success_response(result)
    except Exception as e:
        return ResponseManager.error_response(str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/{user_id}",
               tags=["User"],
               responses={
                   200: {"description": "User deleted successfully"},
                   404: {"model": ResponseError, "description": "User not found"},
                   500: {"model": ResponseError, "description": "Internal server error."},
               })
async def delete_user(user_id: str):
    """
    Deletes a user.

    Args:
        user_id: ID of the user to delete

    Returns:
        dict: Confirmation message
    """
    try:
        result = await service.delete_user(user_id)
        if not result:
            return ResponseManager.error_response("User not found", status_code=status.HTTP_404_NOT_FOUND)
        return ResponseManager.success_response({"message": "User deleted successfully"})
    except Exception as e:
        return ResponseManager.error_response(str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/login",
             tags=["Auth"],
             responses={
                 200: {"model": User, "description": "Login successful"},
                 401: {"model": ResponseError, "description": "Invalid credentials"},
                 500: {"model": ResponseError, "description": "Internal server error."},
             })
async def login(email: str = Body(...), password: str = Body(...)):
    user = await service.login(email, password)
    if not user:
        return ResponseManager.error_response("Invalid credentials", status_code=status.HTTP_401_UNAUTHORIZED)
    return ResponseManager.success_response(user)


# Query management endpoints
@router.post("/{user_id}/queries/{query_id}",
             tags=["User Queries"],
             responses={
                 200: {"model": User, "description": "Query added successfully"},
                 404: {"model": ResponseError, "description": "User not found"},
                 500: {"model": ResponseError, "description": "Internal server error."},
             })
async def add_query(user_id: str, query_id: str):
    """
    Adds a query to a user's queries list.

    Args:
        user_id: ID of the user
        query_id: ID of the query to add

    Returns:
        User: The updated user object
    """
    try:
        result = await service.add_query(user_id, query_id)
        if not result:
            return ResponseManager.error_response("User not found", status_code=status.HTTP_404_NOT_FOUND)
        return ResponseManager.success_response(result)
    except Exception as e:
        return ResponseManager.error_response(str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/{user_id}/queries/{query_id}",
               tags=["User Queries"],
               responses={
                   200: {"model": User, "description": "Query removed successfully"},
                   404: {"model": ResponseError, "description": "User not found"},
                   500: {"model": ResponseError, "description": "Internal server error."},
               })
async def remove_query(user_id: str, query_id: str):
    """
    Removes a query from a user's queries list.

    Args:
        user_id: ID of the user
        query_id: ID of the query to remove

    Returns:
        User: The updated user object
    """
    try:
        result = await service.remove_query(user_id, query_id)
        if not result:
            return ResponseManager.error_response("User not found or query not in list", status_code=status.HTTP_404_NOT_FOUND)
        return ResponseManager.success_response(result)
    except Exception as e:
        return ResponseManager.error_response(str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Alert management endpoints
@router.post("/{user_id}/alerts/{alert_id}",
             tags=["User Alerts"],
             responses={
                 200: {"model": User, "description": "Alert added successfully"},
                 404: {"model": ResponseError, "description": "User not found"},
                 500: {"model": ResponseError, "description": "Internal server error."},
             })
async def add_alert(user_id: str, alert_id: str):
    """
    Adds an alert to a user's alerts list.

    Args:
        user_id: ID of the user
        alert_id: ID of the alert to add

    Returns:
        User: The updated user object
    """
    try:
        result = await service.add_alert(user_id, alert_id)
        if not result:
            return ResponseManager.error_response("User not found", status_code=status.HTTP_404_NOT_FOUND)
        return ResponseManager.success_response(result)
    except Exception as e:
        return ResponseManager.error_response(str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/{user_id}/alerts/{alert_id}",
               tags=["User Alerts"],
               responses={
                   200: {"model": User, "description": "Alert removed successfully"},
                   404: {"model": ResponseError, "description": "User not found"},
                   500: {"model": ResponseError, "description": "Internal server error."},
               })
async def remove_alert(user_id: str, alert_id: str):
    """
    Removes an alert from a user's alerts list.

    Args:
        user_id: ID of the user
        alert_id: ID of the alert to remove

    Returns:
        User: The updated user object
    """
    try:
        result = await service.remove_alert(user_id, alert_id)
        if not result:
            return ResponseManager.error_response("User not found or alert not in list", status_code=status.HTTP_404_NOT_FOUND)
        return ResponseManager.success_response(result)
    except Exception as e:
        return ResponseManager.error_response(str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Credential management endpoints
@router.post("/{user_id}/credentials",
             tags=["User Credentials"],
             responses={
                 200: {"model": User, "description": "Credential added successfully"},
                 404: {"model": ResponseError, "description": "User not found"},
                 500: {"model": ResponseError, "description": "Internal server error."},
             })
async def add_credential(user_id: str, credential: Dict[str, Any] = Body(...)):
    """
    Adds a credential to a user's credentials list.

    Args:
        user_id: ID of the user
        credential: Dict[str, Any] object with database connection information

    Returns:
        User: The updated user object
    """
    try:
        result = await service.add_credential(user_id, credential)
        if not result:
            return ResponseManager.error_response("User not found", status_code=status.HTTP_404_NOT_FOUND)
        return ResponseManager.success_response(result)
    except Exception as e:
        return ResponseManager.error_response(str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/{user_id}/credentials/{credential_index}",
               tags=["User Credentials"],
               responses={
                   200: {"model": User, "description": "Credential removed successfully"},
                   404: {"model": ResponseError, "description": "User not found or invalid index"},
                   400: {"model": ResponseError, "description": "Cannot remove main credential"},
                   500: {"model": ResponseError, "description": "Internal server error."},
               })
async def remove_credential(user_id: str, credential_index: int):
    """
    Removes a credential from a user's credentials list.

    Args:
        user_id: ID of the user
        credential_index: Index of the credential to remove

    Returns:
        User: The updated user object
    """
    try:
        result = await service.remove_credential(user_id, credential_index)
        if not result:
            user = await service.get_user(user_id)
            if not user:
                return ResponseManager.error_response("User not found", status_code=status.HTTP_404_NOT_FOUND)
            elif credential_index < 0 or credential_index >= len(user.credentials):
                return ResponseManager.error_response("Invalid credential index", status_code=status.HTTP_404_NOT_FOUND)
            else:
                return ResponseManager.error_response("Cannot remove main credential", status_code=status.HTTP_400_BAD_REQUEST)
        return ResponseManager.success_response(result)
    except Exception as e:
        return ResponseManager.error_response(str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put("/{user_id}/credentials/{credential_index}/main",
            tags=["User Credentials"],
            responses={
                200: {"model": User, "description": "Main credential set successfully"},
                404: {"model": ResponseError, "description": "User not found or invalid index"},
                500: {"model": ResponseError, "description": "Internal server error."},
            })
async def set_main_credential(user_id: str, credential_index: int):
    """
    Sets a credential as the main credential.

    Args:
        user_id: ID of the user
        credential_index: Index of the credential to set as main

    Returns:
        User: The updated user object
    """
    try:
        result = await service.set_main_credential(user_id, credential_index)
        if not result:
            return ResponseManager.error_response("User not found or invalid credential index", status_code=status.HTTP_404_NOT_FOUND)
        return ResponseManager.success_response(result)
    except Exception as e:
        return ResponseManager.error_response(str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
