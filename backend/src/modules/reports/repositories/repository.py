class ReportRepository:
    def __init__(self):
        pass

    async def column_info(self, column_name: str, table_name: str, schema: str):
        query = f"SELECT {column_name} FROM {schema}.{table_name}"
        return query
