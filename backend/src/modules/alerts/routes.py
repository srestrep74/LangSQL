from fastapi import APIRouter, Depends, status

from src.modules.alerts.models.models import Alert, AlertCreate, AlertPatch
from src.modules.alerts.service import AlertService
from src.utils.ResponseErrorModel import ResponseError
from src.utils.ResponseManager import ResponseManager


router = APIRouter()
alert_service = AlertService()


@router.post("/create", tags=["alerts"], responses={200: {"model": Alert, "description": "Alert created successfully"}, 500: {"model": ResponseError, "description": "Internal Server Error"}})
async def create_alert(alert_data: AlertCreate, alert_service: AlertService = Depends()):
    """
    Creates a new alert in the database.

    Args:
        alert_data (AlertInput): Data required to create the alert.
        alert_service (AlertService, optional): Service instance to handle alert creation. Defaults to Depends().

    Returns:
        Alert: The newly created alert.
    """
    try:
        result = await alert_service.create_alert(alert_data)
        return ResponseManager.success_response(result, status_code=status.HTTP_200_OK)
    except Exception as e:
        return ResponseManager.error_response(str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.patch("/{alert_id}", tags=["alerts"], responses={200: {"model": Alert, "description": "Alert updated successfully"}, 500: {"model": ResponseError, "description": "Internal Server Error"}})
async def update_alert(alert_id: str, alert_data: AlertPatch):
    """
    Updates an alert.

    Args:
        alert_id (str): The ID of the alert to update.
        alert_data (AlertPatch): Data with fields to update.

    Returns:
        Alert: The updated alert.
    """
    try:
        result = await alert_service.update_alert(alert_id, alert_data)
        if result:
            return ResponseManager.success_response(result, status_code=status.HTTP_200_OK)
        return ResponseManager.error_response("Alert not found", status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return ResponseManager.error_response(str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/{alert_id}", tags=["alerts"], responses={200: {"model": Alert, "description": "Alert deleted successfully"}, 404: {"model": ResponseError, "description": "Alert not found"}, 500: {"model": ResponseError, "description": "Internal Server Error"}})
async def delete_alert(alert_id: str, user_id: str):
    """
    Deletes an alert.

    Args:
        alert_id: ID of the alert to delete

    Returns:
        dict: Confirmation message
    """
    try:
        result = await alert_service.delete_alert(alert_id, user_id)
        if result:
            return ResponseManager.success_response({"message": "Alert deleted successfully"})
        return ResponseManager.error_response("Alert not found", status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return ResponseManager.error_response(str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/{alert_id}", tags=["alerts"], responses={200: {"model": Alert, "description": "Alert retrieved successfully"}, 404: {"model": ResponseError, "description": "Alert not found"}, 500: {"model": ResponseError, "description": "Internal Server Error"}})
async def get_alert(alert_id: str):
    """
    Retrieves an alert by its ID.

    Args:
        alert_id (str): The ID of the alert to retrieve.

    Returns:
        Alert: The retrieved alert.
    """
    try:
        result = await alert_service.get_alert(alert_id)
        if result:
            return ResponseManager.success_response(result, status_code=status.HTTP_200_OK)
        return ResponseManager.error_response("Alert not found", status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return ResponseManager.error_response(str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("", tags=["alerts"], responses={200: {"model": list[Alert], "description": "Alerts retrieved successfully"}, 500: {"model": ResponseError, "description": "Internal Server Error"}})
async def get_all_alerts(user_id: str):
    """
    Retrieves all alerts.

    Args:
        user_id (str): The ID of the user whose alerts to retrieve.

    Returns:
        list[Alert]: List of all alerts.
    """
    try:
        alert_service = AlertService()
        result = await alert_service.get_alerts(user_id)
        return ResponseManager.success_response(result, status_code=status.HTTP_200_OK)
    except Exception as e:
        return ResponseManager.error_response(str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
