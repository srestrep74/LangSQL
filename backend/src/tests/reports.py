import json
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient

from app import app
from src.tests.utils.database_connection import database_connection

client = TestClient(app)
connection_dict = database_connection.model_dump()


class TestReportService:
    @patch("src.modules.reports.service.ReportService.create_graph", new_callable=AsyncMock)
    def test_create_graph_success(self, mock_create_graph):
        mock_create_graph.return_value = {
            "status": "success",
            "graph_data": {
                "categories": ["A", "B", "C"],
                "values": [10, 20, 30]
            }
        }

        response = client.post(
            "api/reports/generate-charts",
            data=json.dumps({
                "connection": connection_dict,
                "graph_requests": [
                    {
                            "table": "product",
                            "columns": ["standard_cost"]
                            },
                    {
                        "table": "warehouse",
                        "columns": ["country", "region"]
                    }
                ]
            }, default=str),
            headers={"Content-Type": "application/json"}
        )

        assert response.status_code == 200
        assert response.json()["status"] == "success"
