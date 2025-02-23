from sqlalchemy.orm import Session
from sqlalchemy.sql import text

def get_tables(db: Session, table_schema: str) -> list[str]:
    sql_statement = text(
        """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = :table_schema;
    """)

    result = db.execute(sql_statement, {"table_schema": table_schema}).fetchall()
    return [row[0] for row in result]

def get_attributes(db: Session, table_name: str) -> list[tuple[str, str, str, int | None]]:
    sql_statement = text(
        """
        SELECT column_name, data_type, is_nullable, character_maximum_length
        FROM information_schema.columns
        WHERE table_name = :table_name;
    """)

    result = db.execute(sql_statement, {"table_name": table_name}).fetchall()
    return result

def get_relations(db: Session) -> list[tuple[str, str, str, str]]:
    sql_statement = text(
        """
        SELECT conname AS constraint_name, 
            conrelid::regclass AS table_name, 
            a.attname AS column_name,
            confrelid::regclass AS foreign_table_name
        FROM pg_constraint
        JOIN pg_attribute a ON a.attnum = conkey[1] AND a.attrelid = conrelid
        WHERE contype = 'f';
    """)

    result = db.execute(sql_statement).fetchall()
    return result