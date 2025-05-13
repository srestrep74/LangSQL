from fastapi import APIRouter, Depends
from typing import List


from src.config.dependencies import (
    get_report_service
)

from src.modules.queries.schemas.DatabaseConnection import DatabaseConnection
from src.modules.reports.service import ReportService
from src.modules.reports.schemas.GraphRequest import GraphRequest

router = APIRouter()


@router.post("/generate-charts")
async def generate_charts(
    graph_requests: List[GraphRequest],
    connection: DatabaseConnection,
    service: ReportService = Depends(get_report_service)
):
    result = await service.create_graph(connection, graph_requests)
    return result
