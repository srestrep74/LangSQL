from unittest.mock import AsyncMock, patch

import pytest, json
from datetime import datetime
from fastapi.testclient import TestClient

from app import app
from src.config.constants import Settings
from src.modules.alerts.models.models import AlertCreate
from src.modules.queries.schemas.DatabaseConnection import DatabaseConnection

client = TestClient(app)

database_connection = DatabaseConnection(
    db_type="postgresql",
    host="localhost",
    port=5432,
    username="postgres",
    password="password",
    database_name="test_db",
    schema_name="inventory"
)

class TestAlert:
    @patch("src.modules.alerts.service.AlertRepository")
    def test_create_alert(self, MockAlertRepository):
        mock_alert_repo = MockAlertRepository.return_value
        mock_alert_repo.create_alert = AsyncMock(return_value={
            "id": "mocked_id",
            "user": Settings.TEST_USER,
            "notification_emails": ["test@test.com"],
            "prompt": "Most expensive product",
            "sent": False,
            "expiration_date": datetime.utcnow().isoformat()
        })

        alert_data = AlertCreate(
            notification_emails=["test@test.com"],
            user=Settings.TEST_USER,
            prompt="Most expensive product",
            sent=False,
            expiration_date=datetime.utcnow(),
        )

        alert_dict = alert_data.model_dump()
        alert_dict["expiration_date"] = alert_dict["expiration_date"].isoformat()

        connection_dict = database_connection.model_dump()

        response = client.post(
            "/api/alerts/create",
            data=json.dumps({
                "connection": connection_dict,
                "alert_data": alert_dict
            }, default=str),
            headers={"Content-Type": "application/json"}
        )

        print(response)
        assert response.status_code == 200
        assert response.json()["message"] == "Success"
        assert response.json()["data"]["user"] == alert_dict["user"]
