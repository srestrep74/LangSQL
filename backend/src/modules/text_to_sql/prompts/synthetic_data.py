GENERATE_SYNTHETIC_DATA_PROMPT = (
    """
    You are an SQL database analyst, and your responses must be just SQL statements (not including anything else).
    You are working with a database that contains the following structure: {db_structure}.
    The entire database is within a schema called {schema_name}.

    Generate an INSERT statements with exactly 40 registers for each table (if the table is the result of an n to m relationship, generate an INSERT statements with exactly 20 registers), ensuring that:
    - The inserted data makes logical sense.
    - Previously generated data is taken into account.
    - Names (varchar values) do not exceed 15 characters.
    - Do not duplicate data (specially unique values and primary keys).
    - Be careful of the foreign key constraints, and primary keys.
    """
)
