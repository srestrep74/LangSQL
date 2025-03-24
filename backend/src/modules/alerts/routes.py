from fastapi import APIRouter, Depends, status

from src.modules.alerts.models.models import AlertCreate, Alert, AlertPatch
from src.modules.alerts.service import AlertService
from src.utils.ResponseErrorModel import ResponseError
from src.utils.ResponseManager import ResponseManager

router = APIRouter()


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
async def update_alert(alert_id: str, alert_data: AlertPatch, alert_service: AlertService = Depends()):
    """
    Updates an alert.

    Args:
        alert_id (str): The ID of the alert to update.
        alert_data (AlertPatch): Data with fields to update.
        alert_service (AlertService, optional): Service instance to handle alert creation. Defaults to Depends().

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
async def delete_alert(alert_id: str, alert_service: AlertService = Depends()):
    """
    Deletes an alert.

    Args:
        alert_id: ID of the alert to delete

    Returns:
        dict: Confirmation message
    """
    try:
        result = await alert_service.delete_alert(alert_id)
        if result:
            return ResponseManager.success_response({"message": "Alert deleted successfully"})
        return ResponseManager.error_response("Alert not found", status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return ResponseManager.error_response(str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)