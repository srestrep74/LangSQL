from src.config.database import database
from src.modules.alerts.models.models import AlertCreate, Alert, AlertPatch
from typing import Optional
from bson import ObjectId


class AlertRepository:
    def __init__(self, db=None):
        self.collection = database["Alerts"]

    async def create_alert(self, alert_data: AlertCreate) -> Alert:
        alert_dict = alert_data.model_dump()
        result = await self.collection.insert_one(alert_dict)
        alert_dict["id"] = str(result.inserted_id)
        return Alert(**alert_dict)
    
    async def update_alert(self, alert_id: str, alert_data: AlertPatch) -> Optional[Alert]:
        update_data = {k: v for k, v in alert_data.dict().items() if v is not None}
        
        if not update_data:
            return await self.get_by_id(alert_id)

        try:
            result = await self.collection.update_one({"_id": ObjectId(alert_id)}, {"$set": update_data})
            if result.matched_count:
                return await self.get_by_id(alert_id)
            return None
        except Exception as e:
            return None

    async def get_by_id(self, alert_id: str) -> Optional[Alert]:
        try:
            alert = await self.collection.find_one({"_id": ObjectId(alert_id)})
            if alert:
                alert["id"] = str(alert["_id"])
                del alert["_id"]
                return Alert(**alert)
            
            return None
        except Exception as e:
            return None
        
    async def delete_alert(self, alert_id: str) -> bool:
        try:
            result = await self.collection.delete_one({"_id": ObjectId(alert_id)})
            return result.deleted_count > 0
        except Exception:
            return False