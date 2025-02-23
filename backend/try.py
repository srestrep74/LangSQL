from src.modules.text_to_sql.service import LangToSqlService

db_structure = """
Tables:
- users (id, name, email, created_at)
- orders (id, user_id, amount, status, created_at)
- products (id, name, price, stock)

Relationships:
- users.id -> orders.user_id (One-to-Many)
- orders.id -> products.id (Many-to-Many through order_items)
"""

chat_service = LangToSqlService(db_structure)

chat_service.conversation()