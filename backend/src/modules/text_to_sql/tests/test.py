from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from app import app

client = TestClient(app)


class TestSyntheticDataEndpoint:
    @patch("src.modules.text_to_sql.service.SyntheticDataModelService.generate_synthetic_data")
    def test_generate_synthetic_data_endpoint(self, mock_generate_synthetic_data):
        # Setup the mock to return some fake SQL
        mock_generate_synthetic_data.return_value = "INSERT INTO users (name, email) VALUES ('Test User', 'test@example.com');"
        
        # Make the request to the endpoint
        response = client.post("/api/text-to-sql/generate_synthetic_data")
        
        # Check that the endpoint returns a 200 OK status code
        assert response.status_code == 200
        
        # Check that the response contains the expected structure
        response_json = response.json()
        assert response_json["status"] == "success"
        assert response_json["message"] == "Success"
        assert "results" in response_json["data"]
        
        # Verify that the service method was called with iterations=1
        mock_generate_synthetic_data.assert_called_once_with(iterations=1)