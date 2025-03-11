from fastapi import Depends
from .repositories import AlertRepository
from .models import AlertInput, AlertDB
from src.adapters.text_to_sql.adapter import TextToSQLAdapter
from src.config.dependencies import get_text_to_sql_adapter


class AlertService:
    def __init__(self, text_to_sql_adapter: TextToSQLAdapter = Depends(get_text_to_sql_adapter), alert_repository: AlertRepository = Depends()):
        self.text_to_sql_adapter = text_to_sql_adapter
        self.alert_repository = alert_repository

    async def create_alert(self, alert_data: AlertInput) -> AlertDB:
        sql_query = self.text_to_sql_adapter.get_response(alert_data.prompt, "inventory")
        alert_db = AlertDB(**alert_data.dict(), user="Alert User", sql_query=sql_query)
        return await self.alert_repository.create_alert(alert_db)