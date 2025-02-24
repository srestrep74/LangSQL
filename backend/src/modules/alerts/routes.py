from fastapi import APIRouter, Depends
from .controllers import AlertController
from .models import AlertInput, AlertDB
from typing import List

router = APIRouter()

@router.post("/create", response_model=AlertDB)
async def create_alert(alert_data: AlertInput, controller: AlertController = Depends()):
    return await controller.create_alert(alert_data)