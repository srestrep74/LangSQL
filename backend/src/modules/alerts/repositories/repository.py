from ..database import database
from ..models import AlertInput, AlertDB

class AlertRepository:
    def __init__(self, db=None):
        self.collection = database["Alerts"]

    async def create_alert(self, alert_data: AlertInput) -> AlertDB:
        alert_dict = alert_data.model_dump()
        result = await self.collection.insert_one(alert_dict)
        alert_dict["_id"] = str(result.inserted_id)
        return AlertDB(**alert_dict)
    
    async def get_by_id(self, alert_id):
        return await self.db["alerts"].find_one({"_id": alert_id})