from unittest.mock import patch

from fastapi.testclient import TestClient
from unittest.mock import patch
from app import app

client = TestClient(app)


class TestSyntheticDataEndpoint:
    @patch("src.modules.text_to_sql.service.SyntheticDataModelService.generate_synthetic_data")
    def test_generate_synthetic_data_endpoint(self, mock_generate_synthetic_data):
        mock_generate_synthetic_data.return_value = [
            "INSERT INTO inventory.category (id, name) VALUES (361, 'Hardware');"
        ]

        response = client.post(
            "/api/text-to-sql/generate_synthetic_data",
            content={"iterations": 1, "schema_name": "inventory"}
        )

        assert response.status_code == 200

        response_json = response.json()
        assert response_json["status"] == "success"
        assert response_json["message"] == "Success"
        assert "results" in response_json["data"]

        mock_generate_synthetic_data.assert_called_once_with(iterations=1, schema_name="inventory")
