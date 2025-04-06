import httpx
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from src.modules.alerts.service import AlertService

class CronJob:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.trigger = CronTrigger(second="*/20")
        self.scheduler.add_job(self.trigger_alert_check, self.trigger)

    async def trigger_alert_check(self):
        """Calls the alert check endpoint"""
        async with httpx.AsyncClient() as client:
            try:
                print("Calling alert check...")
                alert_service = AlertService()
                await alert_service.check_alerts()
            except Exception as e:
                print(f"Error calling alert check: {str(e)}")

    def start(self):
        self.scheduler.start()
        print("Cron job scheduler started")