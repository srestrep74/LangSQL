from fastapi import APIRouter, Depends, status
from .models import AlertInput, AlertDB
from .service import AlertService
from src.utils.ResponseManager import ResponseManager

router = APIRouter()

@router.post("/create")
async def create_alert(alert_data: AlertInput, alert_service: AlertService = Depends()):
    """
    Creates a new alert in the database.

    Args:
        alert_data (AlertInput): Data required to create the alert.
        alert_service (AlertService, optional): Service instance to handle alert creation. Defaults to Depends().

    Returns:
        Successful Response (`200 OK`)
        ```json
        {
            "status": "success",
            "message": "succes",
            "data": { "id": 1, "name": "Sample Alert", ... }
        }
        ```

        Error Response (`400 Bad Request`)
        ```json
        {
            "status": "error",
            "message": "Error",
            "details": {"error": "Error description"}
        }
        ```
    """
    try:
        alert = await alert_service.create_alert(alert_data)
        return ResponseManager.success_response(
            data=alert,
            message="success",
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        return ResponseManager.error_response(
            message="Error",
            status_code=status.HTTP_400_BAD_REQUEST,
            details={"error": str(e)},
        )
