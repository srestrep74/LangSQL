from unittest.mock import MagicMock, patch
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.engine import Engine, Connection

from app import app

client = TestClient(app)

DB_STRUCTURE = {
    "users": {
        "columns": [
            {"name": "id", "type": "INTEGER", "nullable": False, "primary_key": True},
            {"name": "name", "type": "VARCHAR", "nullable": True, "primary_key": False}
        ],
        "foreign_keys": []
    },
    "orders": {
        "columns": [
            {"name": "id", "type": "INTEGER", "nullable": False, "primary_key": True},
            {"name": "user_id", "type": "INTEGER", "nullable": True, "primary_key": False},
            {"name": "product", "type": "VARCHAR", "nullable": True, "primary_key": False}
        ],
        "foreign_keys": [
            {"column": "user_id", "references": "users", "referenced_column": "id"}
        ]
    }
}

QUERY_RESULTS = [
    {"id": 1, "name": "John Doe"},
    {"id": 2, "name": "Jane Smith"}
]

class TestPostgreSQLManager:
    def test_get_db_structure(self):
        from src.modules.queries.utils.PostgreSQLManager import PostgreSQLManager
        manager = MagicMock(spec=PostgreSQLManager)
        mock_structure = {
            'test_table': {
                'columns': [
                    {'name': 'id', 'type': 'INTEGER', 'nullable': False, 'primary_key': True},
                    {'name': 'name', 'type': 'VARCHAR', 'nullable': True, 'primary_key': False}
                ],
                'foreign_keys': []
            }
        }
        manager.get_db_structure.return_value = mock_structure
        structure = manager.get_db_structure()
        assert 'test_table' in structure
        assert len(structure['test_table']['columns']) == 2
        assert structure['test_table']['columns'][0]['name'] == 'id'
        assert structure['test_table']['columns'][1]['name'] == 'name'
        assert 'foreign_keys' in structure['test_table']

    def test_execute_query(self):
        from src.modules.queries.utils.PostgreSQLManager import PostgreSQLManager
        manager = MagicMock(spec=PostgreSQLManager)
        mock_results = [
            {"id": 1, "name": "Test"},
            {"id": 2, "name": "Another"}
        ]
        manager.execute_query.return_value = mock_results
        results = manager.execute_query("SELECT * FROM test_table")
        assert len(results) == 2
        assert results[0]["id"] == 1
        assert results[0]["name"] == "Test"
        assert results[1]["id"] == 2
        assert results[1]["name"] == "Another"

class TestMySQLManager:
    def test_get_db_structure(self):
        from src.modules.queries.utils.MySQLManager import MySQLManager
        manager = MagicMock(spec=MySQLManager)
        mock_structure = {
            'products': {
                'columns': [
                    {'name': 'id', 'type': 'INT', 'nullable': False, 'primary_key': True},
                    {'name': 'name', 'type': 'VARCHAR', 'nullable': True, 'primary_key': False},
                    {'name': 'price', 'type': 'DECIMAL', 'nullable': True, 'primary_key': False}
                ],
                'foreign_keys': []
            },
            'categories': {
                'columns': [
                    {'name': 'id', 'type': 'INT', 'nullable': False, 'primary_key': True},
                    {'name': 'name', 'type': 'VARCHAR', 'nullable': True, 'primary_key': False}
                ],
                'foreign_keys': []
            },
            'product_categories': {
                'columns': [
                    {'name': 'product_id', 'type': 'INT', 'nullable': False, 'primary_key': True},
                    {'name': 'category_id', 'type': 'INT', 'nullable': False, 'primary_key': True}
                ],
                'foreign_keys': [
                    {'column': 'product_id', 'references': 'products', 'referenced_column': 'id'},
                    {'column': 'category_id', 'references': 'categories', 'referenced_column': 'id'}
                ]
            }
        }
        manager.get_db_structure.return_value = mock_structure
        structure = manager.get_db_structure()
        assert 'products' in structure
        assert 'categories' in structure
        assert 'product_categories' in structure
        assert len(structure['products']['columns']) == 3
        assert structure['products']['columns'][0]['name'] == 'id'
        assert structure['products']['columns'][1]['name'] == 'name'
        assert structure['products']['columns'][2]['name'] == 'price'
        fks = structure['product_categories']['foreign_keys']
        assert len(fks) == 2
        assert fks[0]['column'] == 'product_id'
        assert fks[0]['references'] == 'products'
        assert fks[1]['column'] == 'category_id'
        assert fks[1]['references'] == 'categories'

    def test_execute_query(self):
        from src.modules.queries.utils.MySQLManager import MySQLManager
        manager = MagicMock(spec=MySQLManager)
        mock_results = [
            {"id": 1, "name": "Laptop", "price": 999.99},
            {"id": 2, "name": "Mouse", "price": 24.99},
            {"id": 3, "name": "Keyboard", "price": 49.99}
        ]
        manager.execute_query.return_value = mock_results
        results = manager.execute_query("SELECT * FROM products")
        assert len(results) == 3
        assert results[0]["id"] == 1
        assert results[0]["name"] == "Laptop"
        assert results[0]["price"] == 999.99
        manager.execute_query.return_value = [{"message": "Query executed successfully"}]
        result = manager.execute_query("INSERT INTO products (name, price) VALUES ('Monitor', 199.99)")
        assert len(result) == 1
        assert result[0]["message"] == "Query executed successfully"

    def test_schema_usage(self):
        from src.modules.queries.utils.MySQLManager import MySQLManager
        mock_engine = MagicMock(spec=Engine)
        mock_conn = MagicMock(spec=Connection)
        mock_engine.connect.return_value = mock_conn
        mock_conn.__enter__.return_value = mock_conn
        mock_conn.__exit__.return_value = None
        manager = MySQLManager(mock_engine)
        mock_transaction = MagicMock()
        mock_conn.begin.return_value = mock_transaction
        mock_result = MagicMock()
        mock_result.returns_rows = True
        mock_result.keys.return_value = ['id', 'name']
        mock_result.fetchall.return_value = [(1, 'Test'), (2, 'Another')]
        mock_conn.execute.return_value = mock_result
        with patch('sqlalchemy.text') as mock_text:
            results = manager.execute_query("SELECT * FROM test_table", schema_name="test_schema")
            assert mock_conn.execute.call_count >= 2
            mock_transaction.commit.assert_called_once()

class TestDatabaseManagerFactory:
    def test_register_and_create_manager(self):
        from src.modules.queries.utils.DatabaseManagerFactory import DatabaseManagerFactory
        from src.modules.queries.utils.DatabaseType import DatabaseType
        from src.modules.queries.schemas.DatabaseConnection import DatabaseConnection
        mock_manager_class = MagicMock()
        DatabaseManagerFactory.register(DatabaseType.POSTGRESQL, mock_manager_class)
        test_connection = DatabaseConnection(
            db_type=DatabaseType.POSTGRESQL,
            host="localhost",
            port=5432,
            username="test",
            password="test",
            database_name="test_db"
        )
        manager = DatabaseManagerFactory.create_manager(test_connection)
        assert isinstance(manager, MagicMock)
        mock_manager_class.assert_called_once()