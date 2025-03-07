GENERATE_SYNTHETIC_DATA_PROMPT = (
    """
    You are an SQL database analyst, and your responses should be SQL statements.
    You are working with a database that contains the structure: {db_structure}. The entire database is within a schema called "langsql".

    Generate 60 INSERT statements for each table, ensuring that:
    - The inserted data makes logical sense.
    - Previously generated data is taken into account.
    - Names do not exceed 70 characters.

    For example:

    INSERT INTO suppliers (name, contact, phone) VALUES
    ('SupplierTech', 'Juan Pérez', '555-1234'), -- id 1 | auto-generated
    ('HardwareExpress', 'Ana López', '555-5678'); -- id 2 | auto-generated

    INSERT INTO products (name, description, price, stock) VALUES
    ('Laptop', '15-inch laptop', 1200.00, 10), -- id 1 | auto-generated
    ('Mouse', 'Wireless mouse', 25.50, 50), -- id 2 | auto-generated
    ('Keyboard', 'RGB mechanical keyboard', 80.75, 30); -- id 3 | auto-generated

    INSERT INTO product_suppliers (product_id, supplier_id, quantity_supplied) VALUES
    (1, 1, 5),  -- Laptop from SupplierTech
    (2, 1, 20), -- Mouse from SupplierTech
    (2, 2, 15), -- Mouse from HardwareExpress
    (3, 2, 10); -- Keyboard from HardwareExpress
    """
)
