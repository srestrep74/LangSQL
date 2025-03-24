from fastapi import Depends

from src.adapters.text_to_sql.adapter import TextToSQLAdapter
from src.config.dependencies import get_text_to_sql_adapter
from src.modules.alerts.models.models import Alert, AlertCreate, AlertPatch
from src.modules.alerts.repositories.repository import AlertRepository
from typing import Optional


class AlertService:
    def __init__(self, text_to_sql_adapter: TextToSQLAdapter = Depends(get_text_to_sql_adapter), alert_repository: AlertRepository = Depends()):
        self.text_to_sql_adapter = text_to_sql_adapter
        self.alert_repository = alert_repository

    async def create_alert(self, alert_data: AlertCreate) -> Alert:
        sql_query = self.text_to_sql_adapter.get_response(alert_data.prompt, "inventory")
        alert_data_dict = alert_data.dict(exclude={"sql_query"})
        alert_create = AlertCreate(**alert_data_dict, user="Alert User", sql_query=sql_query)
        return await self.alert_repository.create_alert(alert_create)
    
    async def update_alert(self, alert_id: str, alert_data: AlertPatch) -> Optional[Alert]:
        return await self.alert_repository.update_alert(alert_id, alert_data)
    
    async def delete_alert(self, alert_id: str) -> bool:
        return await self.alert_repository.delete_alert(alert_id)