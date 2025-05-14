from typing import List

from fastapi import APIRouter, Depends, Header

from src.config.dependencies import get_report_service
from src.modules.queries.schemas.DatabaseConnection import DatabaseConnection
from src.modules.reports.schemas.GraphRequest import GraphRequest
from src.modules.reports.service import ReportService

router = APIRouter()


@router.post("/generate-charts")
async def generate_charts(
    graph_requests: List[GraphRequest],
    connection: DatabaseConnection,
    service: ReportService = Depends(get_report_service),
    accept_language: str = Header(default="en")
):
    result = await service.create_graph(connection, graph_requests, accept_language)
    return result
