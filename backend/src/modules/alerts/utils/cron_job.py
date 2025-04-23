import httpx
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from src.adapters.queries.QueryAdapter import QueryAdapter
from src.modules.alerts.service import AlertService
from src.modules.queries.service import QueryService


class CronJob:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.trigger = CronTrigger(second="*/59")
        self.scheduler.add_job(self.trigger_alert_check, self.trigger)

    async def trigger_alert_check(self):
        async with httpx.AsyncClient():
            try:
                query_service = QueryService(db_manager=None)
                query_adapter = QueryAdapter(query_service)
                alert_service = AlertService(query_adapter=query_adapter)
                await alert_service.check_alerts()
                return True
            except Exception as e:
                return False
                print(f"Error calling alert check: {str(e)}")

    def start(self):
        self.scheduler.start()
        print("Cron job scheduler started")
