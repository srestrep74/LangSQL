from unittest.mock import patch

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


class TestSyntheticDataEndpoint:
    @patch("src.modules.text_to_sql.service.SyntheticDataModelService.generate_synthetic_data")
    def test_generate_synthetic_data_endpoint(self, mock_generate_synthetic_data):
        mock_generate_synthetic_data.return_value = "INSERT INTO users (name, email) VALUES ('Test User', 'test@example.com');"

        response = client.post("/api/text-to-sql/generate_synthetic_data")

        assert response.status_code == 200

        response_json = response.json()
        assert response_json["status"] == "success"
        assert response_json["message"] == "Success"
        assert "results" in response_json["data"]

        mock_generate_synthetic_data.assert_called_once_with(iterations=1)
