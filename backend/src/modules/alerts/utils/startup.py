from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.modules.alerts.utils.cron_job import CronJob
from src.modules.alerts.repositories.repository import AlertRepository
from src.adapters.queries.QueryAdapter import QueryAdapter
from src.modules.queries.service import QueryService
from src.modules.queries.utils.DatabaseManager import DatabaseManager
from src.config.constants import Settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_manager = DatabaseManager(Settings.DB_URL)
    query_service = QueryService(db_manager)
    query_adapter = QueryAdapter(query_service)
    alert_repository = AlertRepository()

    cron_job = CronJob(query_adapter, alert_repository)  
    app.state.cron_job = cron_job  
    cron_job.scheduler.start()

    yield  

    cron_job.scheduler.shutdown()
