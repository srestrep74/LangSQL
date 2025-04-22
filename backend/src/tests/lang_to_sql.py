import json
import pytest

from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient

from app import app
from src.modules.queries.schemas.DatabaseConnection import DatabaseConnection
from src.modules.text_to_sql.service import LangToSqlService, SyntheticDataModelService
from src.modules.text_to_sql.utils.APIClientLLMClient import APIClientLLMClient
from src.modules.text_to_sql.models.models import Chat, Message
from src.tests.utils.database_connection import database_connection
from src.tests.utils.mock_db_structure import MOCK_DB_STRUCTURE

client = TestClient(app)


@pytest.fixture
def fake_connection():
    return DatabaseConnection(
        db_type="postgresql",
        username="test_user",
        password="test_pass",
        host="localhost",
        port=5432,
        database_name="test_db",
        schema_name="public"
    )


@pytest.fixture
def fake_chat_data():
    return Chat(
        user_id="user-123",
        messages=[]
    )


@pytest.fixture
def setup_service():
    query_adapter = MagicMock()
    llm_client = MagicMock()
    repository = MagicMock()
    service = LangToSqlService(query_adapter, llm_client, repository)
    return service, query_adapter, llm_client, repository


@pytest.fixture
def mock_service_with_history(self):
    mock_query_adapter = MagicMock()
    mock_query_adapter.get_db_structure.return_value = MOCK_DB_STRUCTURE
    mock_query_adapter.execute_query.return_value = [{"name": "John Doe", "orders": 50}]

    mock_llm_client = MagicMock()
    mock_llm_client.get_model_response.return_value = "SELECT name, COUNT(*) as orders FROM customers JOIN orders ON customers.id = orders.customer_id GROUP BY name ORDER BY orders DESC LIMIT 1"
    mock_llm_client.get_human_response.return_value = "El cliente con más pedidos es:"

    mock_repository = AsyncMock()
    mock_repository.add_message.return_value = True

    mock_messages = [
        Message(role=1, message="¿Cuántos clientes tenemos?"),
        Message(role=0, message="Tenemos 100 clientes\n[{'count': 100}]"),
        Message(role=1, message="¿Cuál es el cliente con más pedidos?")
    ]

    mock_chat = Chat(id="chat123", messages=mock_messages)
    mock_repository.get_chat.return_value = mock_chat

    return LangToSqlService(mock_query_adapter, mock_llm_client, mock_repository)


@pytest.fixture
def mock_service_with_memory():
    mock_query_adapter = MagicMock()
    mock_query_adapter.get_db_structure.return_value = MOCK_DB_STRUCTURE
    mock_query_adapter.execute_query.return_value = [{"total_revenue": 45000.75}]

    mock_llm_client = MagicMock()
    mock_llm_client.get_model_response.return_value = "SELECT SUM(amount) as total_revenue FROM sales WHERE EXTRACT(MONTH FROM date) = 1"
    mock_llm_client.get_human_response.return_value = "En enero, el ingreso total fue:"

    mock_repository = AsyncMock()
    mock_repository.add_message.return_value = True

    previous_messages = [
        Message(role=1, message="¿Cuántas ventas tuvimos en enero?"),
        Message(role=0, message="En enero tuvimos 120 ventas\n[{'month': 'Enero', 'sales': 120}]"),
    ]

    mock_chat = Chat(id="chat123", user_id="user-789", messages=previous_messages)

    mock_repository.get_chat.return_value = mock_chat

    return LangToSqlService(mock_query_adapter, mock_llm_client, mock_repository)


@pytest.mark.asyncio
class TestLangToSqlService:

    async def test_chat_with_complex_query_and_memory(self, setup_service, fake_connection, fake_chat_data):
        service, query_adapter, llm_client, repository = setup_service
        chat_id = "test-chat-id"
        user_input = "List the top 5 products with the highest sales this year, grouped by category."

        repository.create_chat = AsyncMock(return_value=chat_id)
        repository.add_message = AsyncMock(return_value=True)
        repository.get_chat = AsyncMock(return_value=MagicMock(messages=[
            Message(role=1, message="Show me all orders."),
            Message(role=0, message="Here are all orders...")
        ]))

        query_adapter.get_db_structure.return_value = {"tables": ["orders", "products"]}
        query_adapter.execute_query.return_value = [{"product": "Laptop", "sales": 12000}]
        llm_client.get_model_response.return_value = "SELECT product, SUM(sales) FROM orders GROUP BY product LIMIT 5"
        llm_client.get_human_response.return_value = "Here are the top 5 products with highest sales:"

        result = await service.chat(fake_connection, user_input, fake_chat_data, "")

        assert "header" in result
        assert "sql_query" in result
        assert "sql_results" in result
        assert result["header"].startswith("Here are the top 5 products")
        assert "SELECT product" in result["sql_query"]
        assert json.loads(result["sql_results"]) == [{"product": "Laptop", "sales": 12000}]
        llm_client.get_model_response.assert_called_once()
        assert repository.add_message.call_count == 2

    async def test_get_messages_history(self, setup_service):
        service, _, _, repository = setup_service
        repository.get_chat = AsyncMock(return_value=MagicMock(messages=[
            Message(role=1, message="How many customers do we have?"),
            Message(role=0, message="We have 320 customers.")
        ]))

        response = await service.get_messages("some-chat-id")

        assert "messages" in response
        assert len(response["messages"]) == 2
        assert response["messages"][0].message == "How many customers do we have?"

    def test_get_response_generates_sql(self, setup_service, fake_connection):
        service, query_adapter, llm_client, _ = setup_service

        user_input = "How many customers do we have?"

        query_adapter.get_db_structure.return_value = {"tables": ["customers"]}
        llm_client.get_response.return_value = "SELECT COUNT(*) FROM customers"

        response = service.get_response(user_input, fake_connection)

        assert "SELECT COUNT(*)" in response

    async def test_chat_utilizes_query_history(self, setup_service, fake_connection):
        service, query_adapter, llm_client, repository = setup_service
        chat_id = "history-chat"
        user_input = "Show me my recent orders."

        repository.create_chat = AsyncMock(return_value=chat_id)
        repository.add_message = AsyncMock(return_value=True)
        repository.get_chat = AsyncMock(return_value=MagicMock(messages=[
            Message(role=1, message="List all orders"),
            Message(role=0, message="SELECT * FROM orders")
        ]))

        query_adapter.get_db_structure.return_value = {"tables": ["orders"]}
        query_adapter.execute_query.return_value = [{"order_id": 1, "date": "2023-01-01"}]
        llm_client.get_model_response.return_value = "SELECT * FROM orders WHERE date >= '2023-01-01'"
        llm_client.get_human_response.return_value = "Here are your recent orders:"

        chat_data = Chat(user_id="user-456")

        result = await service.chat(fake_connection, user_input, chat_data, "")

        assert "sql_query" in result
        assert "recent orders" in result["header"]

    async def test_conversational_memory_for_follow_up_questions(self, mock_service_with_memory):
        connection = database_connection
        user_input = "¿Y cuánto ingreso generaron esas ventas?"
        chat_id = "chat123"

        chat_data = Chat(id=chat_id, user_id="user-789", messages=[])

        result = await mock_service_with_memory.chat(connection, user_input, chat_data, chat_id)

        assert result is not None
        assert "sql_query" in result
        assert "sql_results" in result
        assert "header" in result
        assert result["header"] == "En enero, el ingreso total fue:"
        assert "MONTH" in result["sql_query"]
        assert "= 1" in result["sql_query"]
        mock_service_with_memory.repository.get_chat.assert_called_once_with(chat_id)
        assert mock_service_with_memory.repository.add_message.call_count == 2


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
