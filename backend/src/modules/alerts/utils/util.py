from fastapi import Depends
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from src.modules.alerts.repositories.repository import AlertRepository
from src.adapters.queries.QueryAdapter import QueryAdapter
from src.modules.queries.service import QueryService


class CronJob:
    def __init__(self, query_adapter: QueryAdapter, alert_repository: AlertRepository):
        self.scheduler = AsyncIOScheduler()
        self.trigger = CronTrigger(second="*/10")
        self.scheduler.add_job(self.check_alert, self.trigger)
        self.query_adapter = query_adapter
        self.alert_repository = alert_repository


    async def check_alert(self):
        """Check if the alert is expired and perform necessary actions."""
        try:
            alerts = await self.alert_repository.get_all_alerts()
            for alert in alerts:
                query_result = await self.query_adapter.execute_query(alert.sql_query, "inventory")
                print(f"Alert ID: {alert.id}, Query Result: {query_result}")
        except Exception as e:
            print(f"Error in check_alert: {e}")