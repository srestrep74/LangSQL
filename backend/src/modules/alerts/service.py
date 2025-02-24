from .repositories import AlertRepository
from .models import AlertInput, AlertDB
from fastapi import Depends

class AlertService:
    def __init__(self, alert_repository: AlertRepository = Depends()):
        self.alert_repository = alert_repository

    async def create_alert(self, alert_data: AlertInput) -> AlertDB:
        return await self.alert_repository.create_alert(alert_data)