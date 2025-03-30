from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from src.modules.alerts.repositories.repository import AlertRepository
from src.adapters.queries.QueryAdapter import QueryAdapter
from src.modules.alerts.utils.email_sender import EmailSender


class CronJob:
    def __init__(self, query_adapter: QueryAdapter, alert_repository: AlertRepository, email_sender: EmailSender = EmailSender()):
        self.scheduler = AsyncIOScheduler()
        self.trigger = CronTrigger(second="*/20")
        self.scheduler.add_job(self.check_alert, self.trigger)
        self.query_adapter = query_adapter
        self.alert_repository = alert_repository
        self.email_sender = email_sender

    async def check_alert(self):
        """Check if the alert is expired and perform necessary actions."""
        try:
            alerts = await self.alert_repository.get_all_alerts()
            for alert in alerts:
                query_result = self.query_adapter.execute_query(alert.sql_query, "inventory") # Assuming "inventory" is the schema name, this should be replace
                if query_result:
                    await self.email_sender.send_email(alert.notification_emails, alert.prompt)
        except Exception as e:
            print(f"Error in check_alert: {e}")