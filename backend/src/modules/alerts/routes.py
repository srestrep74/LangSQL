from fastapi import APIRouter, Depends
from .models import AlertInput, AlertDB
from .service import AlertService

router = APIRouter()

@router.post("/create", response_model=AlertDB)
async def create_alert(alert_data: AlertInput, alert_service: AlertService = Depends()):
    """
    Creates a new alert in the database.

    Args:

        alert_data (AlertInput): Data required to create the alert.

        alert_service (AlertService, optional): Service instance to handle alert creation. Defaults to Depends().

    Returns:
    
        AlertDB: The created alert with its assigned ID.
    """
    return await alert_service.create_alert(alert_data)