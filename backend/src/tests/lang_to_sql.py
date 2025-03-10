from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from app import app
from src.modules.text_to_sql.service import SyntheticDataModelService
from src.modules.text_to_sql.utils.APIClientLLMClient import APIClientLLMClient
from src.tests.utils.mock_db_structure import MOCK_DB_STRUCTURE

client = TestClient(app)


class TestSyntheticData:
    @patch("src.modules.text_to_sql.service.SyntheticDataModelService.generate_synthetic_data")
    def test_generate_synthetic_data_endpoint(self, mock_generate_synthetic_data):
        mock_generate_synthetic_data.return_value = [
            "INSERT INTO inventory.category (id, name) VALUES (361, 'Hardware');"
        ]

        response = client.post(
            "/api/text-to-sql/generate_synthetic_data",
            json={"iterations": 1, "schema_name": "inventory"}
        )

        assert response.status_code == 200

        response_json = response.json()
        assert response_json["status"] == "success"
        assert response_json["message"] == "Success"
        assert "results" in response_json["data"]

        mock_generate_synthetic_data.assert_called_once_with(iterations=1, schema_name="inventory")

    @pytest.fixture
    def mock_synthetic_data_service(self):
        mock_query_adapter = MagicMock()
        mock_query_adapter.get_db_structure.return_value = MOCK_DB_STRUCTURE
        mock_query_adapter.execute_query.return_value = None

        llm_client = APIClientLLMClient()

        return SyntheticDataModelService(mock_query_adapter, llm_client)

    def test_generate_synthetic_data_service(self, mock_synthetic_data_service):
        response = mock_synthetic_data_service.generate_synthetic_data(iterations=40, schema_name="test")

        assert isinstance(response, str)
        assert "INSERT INTO" in response
