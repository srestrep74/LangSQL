from typing import Optional, Any

from fastapi import Depends

from src.adapters.text_to_sql.adapter import TextToSQLAdapter
from src.config.dependencies import get_text_to_sql_adapter, get_query_adapter
from src.modules.alerts.models.models import Alert, AlertCreate, AlertPatch
from src.modules.alerts.repositories.repository import AlertRepository
from src.modules.alerts.utils.email_sender import EmailSender
from src.adapters.queries.QueryAdapter import QueryAdapter
import httpx


class AlertService:
    def __init__(self,  query_adapter: QueryAdapter = Depends(get_query_adapter), text_to_sql_adapter: TextToSQLAdapter = Depends(get_text_to_sql_adapter), alert_repository: AlertRepository = Depends(), email_sender: EmailSender = Depends()):
        self.text_to_sql_adapter = text_to_sql_adapter
        self.alert_repository = AlertRepository()
        self.email_sender = email_sender
        self.query_adapter = query_adapter

    async def create_alert(self, alert_data: AlertCreate) -> Alert:
        #sql_query = self.text_to_sql_adapter.get_response(alert_data.prompt, "inventory")
        alert_data_dict = alert_data.model_dump(exclude={"sql_query"})
        alert_create = AlertCreate(**alert_data_dict, sql_query=None)

        saved_alert = await self.alert_repository.create_alert(alert_create)

        user_id = alert_data.user
        alert_id = saved_alert.id
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(f"http://127.0.0.1:8000/api/auth/{user_id}/alerts/{alert_id}")
            except Exception as e:
                print(f"Error calling alert check: {str(e)}")

        return saved_alert

    async def update_alert(self, alert_id: str, alert_data: AlertPatch) -> Optional[Alert]:
        return await self.alert_repository.update_alert(alert_id, alert_data)

    async def delete_alert(self, alert_id: str, user_id: str) -> bool:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.delete(f"http://127.0.0.1:8000/api/auth/{user_id}/alerts/{alert_id}")
            except Exception as e:
                print(f"Error calling alert check: {str(e)}")
        return await self.alert_repository.delete_alert(alert_id)
    
    async def get_alert(self, alert_id: str) -> Optional[Alert]:
        return await self.alert_repository.get_by_id(alert_id)
    
    async def get_all_alerts(self, user_id: str) -> list[Alert]:
        result = await self.alert_repository.get_all_alerts(user_id)
        return result
    
    async def check_alert(self):
        try:
            print("Checking alerts...")
            alerts = await self.get_all_alerts()
            for alert in alerts:
                query_result = self.query_adapter.execute_query(alert.sql_query, "inventory") # Assuming "inventory" is the schema name, this should be replace
                if query_result:
                    await self.email_sender.send_email(alert.notification_emails, alert.prompt)
        except Exception as e:
            print(f"Error in check_alert: {e}")
