from unittest.mock import AsyncMock, patch
import asyncio
import pytest
import json
from datetime import datetime

from fastapi.testclient import TestClient

from app import app
from src.config.constants import Settings
from src.modules.alerts.models.models import AlertCreate, Alert
from src.modules.alerts.utils.cron_job import CronJob
from src.modules.queries.schemas.DatabaseConnection import DatabaseConnection
from src.tests.utils.database_connection import database_connection
from src.modules.alerts.routes import alert_service

client = TestClient(app)



class TestAlert:
    @patch("src.modules.alerts.service.AlertRepository")
    def test_create_alert(self, MockAlertRepository):
        mock_alert_repo = MockAlertRepository.return_value
        mock_alert_repo.create_alert = AsyncMock(return_value=Alert(
            id="mocked_id",
            user=Settings.TEST_USER,
            notification_emails=["test@test.com"],
            prompt="Most expensive product",
            sent=False,
            expiration_date=datetime.utcnow().isoformat()
        ))

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

        print(response.json())
        assert response.status_code == 200
        assert response.json()["message"] == "Success"

    @patch("src.modules.alerts.service.AlertService.get_sql_query", new_callable=AsyncMock)
    def test_update_alert(self, mock_get_sql_query):
        mock_get_sql_query.return_value = None

        updated_alert = Alert(
            id=Settings.TEST_ALERT,
            user=Settings.TEST_USER,
            notification_emails=["updated@test.com"],
            prompt="Updated prompt",
            sent=True,
            expiration_date=datetime.utcnow().isoformat(),
            sql_query=None
        )

        with patch.object(alert_service, "alert_repository") as mock_repo:
            mock_repo.get_by_id = AsyncMock(return_value=updated_alert)
            mock_repo.update_alert = AsyncMock(return_value=updated_alert)

            alert_patch_data = {
                "notification_emails": ["updated@test.com"],
                "prompt": "Updated prompt"
            }

            connection_dict = database_connection.model_dump()

            response = client.patch(
                f"/api/alerts/{Settings.TEST_ALERT}",
                data=json.dumps({
                    "connection": connection_dict,
                    "alert_data": alert_patch_data
                }, default=str),
                headers={"Content-Type": "application/json"}
            )

            print(response.json())
            assert response.status_code == 200
            assert response.json()["message"] == "Success"

    @patch("src.modules.alerts.service.EmailSender.send_email", new_callable=AsyncMock)
    @patch("src.modules.alerts.service.AlertRepository.update_alert", new_callable=AsyncMock)
    @patch("src.modules.alerts.service.AlertRepository.get_alerts", new_callable=AsyncMock)
    @patch("src.modules.auth.repositories.repository.UserRepository.get_by_id", new_callable=AsyncMock)
    def test_check_alert(self, mock_get_user_by_id, mock_get_alerts, mock_update_alert, mock_send_email):
        mock_get_alerts.return_value = [
            Alert(
                id=Settings.TEST_ALERT,
                user=Settings.TEST_USER,
                notification_emails=["test@test.com"],
                prompt="Check if inventory is low",
                sent=False,
                expiration_date=datetime.utcnow().isoformat(),
                sql_query="SELECT * FROM inventory WHERE stock < 10"
            )
        ]

        mock_get_user_by_id.return_value = type("User", (), {
            "credentials": [{
                "dbType": "postgresql",
                "host": "localhost",
                "port": 5432,
                "user": "postgres",
                "password": "password",
                "db_name": "test_db"
            }]
        })()

        with patch("src.modules.alerts.service.QueryAdapter.execute_query", return_value=[{"id": 1}]):
            cron_job = CronJob()
            result = asyncio.run(cron_job.trigger_alert_check())
            assert result is True

        mock_send_email.assert_called_once()
        mock_update_alert.assert_called_once()
