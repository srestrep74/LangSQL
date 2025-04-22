from src.modules.queries.schemas.DatabaseConnection import DatabaseConnection

database_connection = DatabaseConnection(
    db_type="postgresql",
    host="localhost",
    port=5432,
    username="postgres",
    password="password",
    database_name="test_db",
    schema_name="inventory"
)
