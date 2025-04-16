from unittest.mock import MagicMock, patch

import pytest, json
from datetime import datetime
from fastapi.testclient import TestClient

from app import app
from src.modules.alerts.models.models import AlertCreate
from src.modules.text_to_sql.utils.APIClientLLMClient import APIClientLLMClient
from src.tests.utils.mock_db_structure import MOCK_DB_STRUCTURE
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
    def test_create_alert(self):
        alert_data = AlertCreate(
            notification_emails=["test@test.com"],
            user="test_user",
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

        assert response.status_code == 200
        assert response.json()["message"] == "Success"
        assert response.json()["data"]["user"] == alert_dict["user"]

        alert_id = response.json()["data"]["id"]
        response = client.delete(
            f"/api/alerts/{alert_id}?user_id={alert_dict['user']}"
        )
