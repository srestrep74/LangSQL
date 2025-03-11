from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


class TestAlerts:
    def test_create_alerts(self):
        response = client.post(
            "/api/alerts/create",
            json={"notification_emails": ["test@example.com"], "prompt": "The most expensive product", "expiration_date": "2025-12-31T12:00:00"},
        )

        assert response.status_code == 200

        response_json = response.json()
        assert response_json["status"] == "success"
        assert response_json["message"] == "success"
        assert "sql_query" in response_json["data"]