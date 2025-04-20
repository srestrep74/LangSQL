from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.modules.alerts.utils.cron_job import CronJob


@asynccontextmanager
async def lifespan(app: FastAPI):
    cron_job = CronJob()
    app.state.cron_job = cron_job
    cron_job.start()

    yield

    cron_job.scheduler.shutdown()
