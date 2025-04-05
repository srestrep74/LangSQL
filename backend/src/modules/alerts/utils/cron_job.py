import httpx
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

class CronJob:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.trigger = CronTrigger(second="*/20")
        self.scheduler.add_job(self.trigger_alert_check, self.trigger)

    async def trigger_alert_check(self):
        """Calls the alert check endpoint"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get("http://127.0.0.1:8000/api/alerts/check")
                if response.status_code == 200:
                    print("Alert check triggered successfully")
                else:
                    print(f"Alert check failed with status {response.status_code}: {response.text}")
            except Exception as e:
                print(f"Error calling alert check: {str(e)}")

    def start(self):
        self.scheduler.start()
        print("Cron job scheduler started")