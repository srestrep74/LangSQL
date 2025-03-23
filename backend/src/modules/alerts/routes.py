from fastapi import APIRouter, Depends, status

from src.modules.alerts.models.models import AlertCreate, Alert
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
