from src.config.database import database
from src.modules.alerts.models.models import Alert, AlertCreate


class AlertRepository:
    def __init__(self, db=None):
        self.collection = database["Alerts"]

    async def create_alert(self, alert_data: AlertCreate) -> Alert:
        alert_dict = alert_data.model_dump()
        result = await self.collection.insert_one(alert_dict)
        alert_dict["id"] = str(result.inserted_id)
        return Alert(**alert_dict)
