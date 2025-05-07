from typing import Optional
from datetime import datetime

import httpx
from fastapi import Depends

from src.adapters.queries.QueryAdapter import QueryAdapter
from src.adapters.text_to_sql.adapter import TextToSQLAdapter
from src.config.constants import Settings
from src.config.dependencies import get_query_adapter, get_text_to_sql_adapter
from src.modules.alerts.models.models import Alert, AlertCreate, AlertPatch
from src.modules.alerts.repositories.repository import AlertRepository
from src.modules.alerts.utils.email_sender import EmailSender
from src.modules.auth.repositories.repository import UserRepository
from src.modules.queries.schemas.DatabaseConnection import DatabaseConnection

api_url = Settings().API_URL


class AlertService:
    def __init__(self, text_to_sql_adapter: TextToSQLAdapter = Depends(get_text_to_sql_adapter), query_adapter: QueryAdapter = Depends(get_query_adapter)):
        self.text_to_sql_adapter = text_to_sql_adapter
        self.alert_repository = AlertRepository()
        self.email_sender = EmailSender()
        self.query_adapter = query_adapter

    async def get_sql_query(self, prompt: str, connection: DatabaseConnection) -> str:
        return self.text_to_sql_adapter.get_response(prompt, connection)

    async def create_alert(self, alert_data: AlertCreate, connection: DatabaseConnection) -> Alert:
        sql_query = await self.get_sql_query(alert_data.prompt, connection)
        alert_data_dict = alert_data.model_dump(exclude={"sql_query"})
        alert_create = AlertCreate(**alert_data_dict, sql_query=sql_query)

        saved_alert = await self.alert_repository.create_alert(alert_create)

        user_id = alert_data.user
        alert_id = saved_alert.id

        async with httpx.AsyncClient() as client:
            try:
                await client.post(f"{api_url}/auth/{user_id}/alerts/{alert_id}")
            except Exception as e:
                print(f"Error calling alert check: {str(e)}")

        return saved_alert

    async def update_alert(self, alert_id: str, alert_data: AlertPatch, connection: DatabaseConnection) -> Optional[Alert]:
        existing_alert = await self.alert_repository.get_by_id(alert_id)

        if alert_data.prompt != existing_alert.prompt:
            sql_query = await self.get_sql_query(alert_data.prompt, connection)
            alert_data_dict = alert_data.model_dump(exclude={"sql_query"})
            alert_data = AlertPatch(**alert_data_dict, sql_query=sql_query)

        return await self.alert_repository.update_alert(alert_id, alert_data)

    async def delete_alert(self, alert_id: str, user_id: str) -> bool:
        async with httpx.AsyncClient() as client:
            try:
                await client.delete(f"{api_url}/auth/{user_id}/alerts/{alert_id}")
            except Exception as e:
                print(f"Error calling alert check: {str(e)}")
        return await self.alert_repository.delete_alert(alert_id)

    async def get_alert(self, alert_id: str) -> Optional[Alert]:
        return await self.alert_repository.get_by_id(alert_id)

    async def get_alerts(self, user_id: str) -> list[Alert]:
        result = await self.alert_repository.get_alerts(user_id)
        return result

    async def check_alerts(self):
        try:
            alerts = await self.alert_repository.get_alerts()
            for alert in alerts:
                if alert.sent:
                    continue
                if alert.expiration_date and datetime.now() > alert.expiration_date:
                    continue
                try:
                    user_id = alert.user
                    user_repository = UserRepository()
                    user = await user_repository.get_by_id(user_id)

                    db_connection = DatabaseConnection(
                        db_type=user.credentials[0]["dbType"],
                        host=user.credentials[0]["host"],
                        port=user.credentials[0]["port"],
                        username=user.credentials[0]["user"],
                        password=user.credentials[0]["password"],
                        database_name=user.credentials[0]["db_name"],
                        schema_name=user.credentials[0]["db_name"],
                    )

                    query_result = self.query_adapter.execute_query(alert.sql_query, db_connection)

                    if query_result:
                        await self.email_sender.send_email(alert.notification_emails, alert.prompt)
                        updated_alert = AlertPatch(sent=True)
                        await self.alert_repository.update_alert(alert.id, updated_alert)

                except Exception as alert_error:
                    print(f"Failed to process alert {alert.id}: {alert_error}")
        except Exception as e:
            print(f"Error in check_alert: {e}")
