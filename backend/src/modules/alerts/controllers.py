from fastapi import Depends
from .service import AlertService
from .models import AlertInput, AlertDB

class AlertController:
    def __init__(self, alert_service: AlertService = Depends()):
        self.alert_service = alert_service

    async def create_alert(self, alert_data: AlertInput) -> AlertDB:
        return await self.alert_service.create_alert(alert_data)
