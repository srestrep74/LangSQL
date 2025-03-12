MOCK_DB_STRUCTURE = {
    "category": {
        "columns": [
            {"name": "id", "type": "INTEGER", "nullable": False, "primary_key": True},
            {"name": "name", "type": "VARCHAR(100)", "nullable": False, "primary_key": False},
            {"name": "description", "type": "TEXT", "nullable": True, "primary_key": False}
        ],
        "foreign_keys": []
    },
    "supplier": {
        "columns": [
            {"name": "id", "type": "INTEGER", "nullable": False, "primary_key": True},
            {"name": "name", "type": "VARCHAR(150)", "nullable": False, "primary_key": False},
            {"name": "contact", "type": "VARCHAR(100)", "nullable": True, "primary_key": False},
            {"name": "phone", "type": "VARCHAR(20)", "nullable": True, "primary_key": False},
            {"name": "email", "type": "VARCHAR(100)", "nullable": True, "primary_key": False}
        ],
        "foreign_keys": []
    },
    "product": {
        "columns": [
            {"name": "id", "type": "INTEGER", "nullable": False, "primary_key": True},
            {"name": "name", "type": "VARCHAR(150)", "nullable": False, "primary_key": False},
            {"name": "description", "type": "TEXT", "nullable": True, "primary_key": False},
            {"name": "price", "type": "NUMERIC(10, 2)", "nullable": False, "primary_key": False},
            {"name": "stock", "type": "INTEGER", "nullable": False, "primary_key": False},
            {"name": "category_id", "type": "INTEGER", "nullable": False, "primary_key": False},
            {"name": "supplier_id", "type": "INTEGER", "nullable": False, "primary_key": False}
        ],
        "foreign_keys": [
            {"column": "supplier_id", "references": "supplier", "referenced_column": "id"},
            {"column": "category_id", "references": "category", "referenced_column": "id"}
        ]
    }
}
