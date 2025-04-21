from unittest.mock import MagicMock, patch

import pytest
import json
from fastapi.testclient import TestClient

from app import app
from src.modules.text_to_sql.service import SyntheticDataModelService, LangToSqlService
from src.modules.text_to_sql.utils.APIClientLLMClient import APIClientLLMClient
from src.tests.utils.mock_db_structure import MOCK_DB_STRUCTURE
from src.modules.queries.schemas.DatabaseConnection import DatabaseConnection
from src.tests.utils.database_connection import database_connection

client = TestClient(app)


class TestLangToSqlService:
    @pytest.fixture
    def mock_service(self):
        mock_query_adapter = MagicMock()
        mock_query_adapter.get_db_structure.return_value = {"tables": ["products", "categories"]}
        mock_query_adapter.execute_query.return_value = {"columns": ["id", "name"], "rows": [[1, "Test"]]}

        mock_llm_client = MagicMock()
        mock_llm_client.get_model_response.return_value = "SELECT * FROM inventory.categories;"
        mock_llm_client.get_human_response.return_value = "Aquí están las categorías:"

        mock_repository = MagicMock()
        mock_repository.create_chat = MagicMock(return_value="test_chat_id")
        mock_repository.add_message = MagicMock(return_value=True)
        mock_repository.get_chat = MagicMock(return_value={"id": "test_chat_id", "user_id": "test_user", "messages": []})

        service = LangToSqlService(
            query_adapter=mock_query_adapter,
            llm_client=mock_llm_client,
            TextToSqlRepository=mock_repository
        )

        service.chat = MagicMock(return_value={
            "header": "Aquí están las categorías:",
            "sql_query": "SELECT * FROM inventory.categories;",
            "sql_results": json.dumps({"columns": ["id", "name"], "rows": [[1, "Test"]]})
        })

        return service

    def test_successful_response_format(self, mock_service):
        result = mock_service.chat(
            connection=DatabaseConnection,
            user_input="Muestra todas las categorías",
            chat_data={"name": "Test Chat", "user_id": "test_user"},
            chat_id="test_chat_id"
        )

        assert "header" in result, "The response must contain a 'header' field"
        assert "sql_query" in result, "The response must contain a 'sql_query' field"
        assert "sql_results" in result, "The response must contain a 'sql_results' field"

        assert "error" not in result, "The response must not contain errors"

        assert result["header"], "The 'header' field must not be empty"
        assert result["sql_query"], "The 'sql_query' field must not be empty"
        assert result["sql_results"], "The 'sql_results' field must not be empty"

        try:
            parsed_results = json.loads(result["sql_results"])
            assert "columns" in parsed_results, "SQL results must contain columns"
            assert "rows" in parsed_results, "SQL results must contain rows"
        except json.JSONDecodeError:
            pytest.fail("sql_results must be valid JSON")


class TestSyntheticData:
    @patch("src.modules.text_to_sql.service.SyntheticDataModelService.generate_synthetic_data")
    def test_generate_synthetic_data_endpoint(self, mock_generate_synthetic_data):
        mock_generate_synthetic_data.return_value = [
            "INSERT INTO inventory.category (id, name) VALUES (361, 'Hardware');"
        ]

        response = client.post(
            "/api/text-to-sql/generate_synthetic_data",
            json={"iterations": 1, "connection": database_connection.model_dump()}
        )

        assert response.status_code == 200

        response_json = response.json()
        assert response_json["status"] == "success"
        assert response_json["message"] == "Success"
        assert "results" in response_json["data"]

        mock_generate_synthetic_data.assert_called_once_with(1, database_connection)

    @pytest.fixture
    def mock_synthetic_data_service(self):
        mock_query_adapter = MagicMock()
        mock_query_adapter.get_db_structure.return_value = MOCK_DB_STRUCTURE
        mock_query_adapter.execute_query.return_value = None

        llm_client = APIClientLLMClient()

        return SyntheticDataModelService(mock_query_adapter, llm_client)

    def test_generate_synthetic_data_service(self, mock_synthetic_data_service):
        response = mock_synthetic_data_service.generate_synthetic_data(iterations=40, connection=database_connection)

        assert isinstance(response, str)
        assert "INSERT INTO" in response
