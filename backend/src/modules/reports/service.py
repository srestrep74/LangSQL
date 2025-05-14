from typing import List, Dict

import pandas as pd

from src.adapters.queries.QueryAdapter import QueryAdapter
from src.modules.queries.schemas.DatabaseConnection import DatabaseConnection
from src.modules.reports.repositories.repository import ReportRepository
from src.modules.reports.utils.graph_factory import GraphFactory
from src.modules.reports.schemas.GraphRequest import GraphRequest
from src.modules.reports.utils.graph_factory import GRAPH_SUGGESTIONS
from src.modules.reports.utils.AdditionalInfo import AdditionalInfoClient


class ReportService:
    def __init__(self, report_repository: ReportRepository, query_adapter: QueryAdapter) -> None:
        self.report_repository = report_repository
        self.query_adapter = query_adapter

    async def infer_column_types(self, df: pd.DataFrame) -> dict:
        column_type = ""

        for col in df.columns:
            unique_vals = df[col].dropna().unique()
            num_unique = len(unique_vals)

            if pd.api.types.is_numeric_dtype(df[col]):
                if num_unique <= 10:
                    column_type = "categorical"
                else:
                    column_type = "numerical"
            elif pd.api.types.is_datetime64_any_dtype(df[col]):
                column_type = "datetime"
            elif pd.api.types.is_string_dtype(df[col]):
                if num_unique <= 20:
                    column_type = "categorical"
                else:
                    column_type = "text"
            else:
                column_type = "unknown"

        return column_type

    async def get_table_data(self, connection: DatabaseConnection, table_name: str, column_name: str, schema: str) -> pd.DataFrame:
        sql_query = await self.report_repository.column_info(column_name, table_name, schema)
        info = self.query_adapter.execute_query(sql_query, connection)
        df = pd.DataFrame(info)
        return df

    async def extract_language(self, accept_language: str) -> str:
        return accept_language.split(',')[0].split(';')[0].strip()

    async def create_graph(
        self, connection: DatabaseConnection, graph_requests: List[GraphRequest], accept_language: str
    ) -> Dict[str, dict]:
        graphs_output = {}
        schema = connection.schema_name

        language = await self.extract_language(accept_language)

        for request in graph_requests:
            table_name = request.table
            columns = request.columns

            for col in columns:
                df = await self.get_table_data(connection, table_name, col, schema)
                column_type = await self.infer_column_types(df)

                graph_classes = GraphFactory.get_graphs(column_type)
                column_graphs = []

                if column_type not in GRAPH_SUGGESTIONS:
                    column_graphs = "No Charts available for this type of data."
                else:
                    for graph_cls in graph_classes:
                        graph_instance = graph_cls()
                        chart_config = graph_instance.generate(col, df)

                        info_client = AdditionalInfoClient()
                        additional_info = info_client.get_additional_info(chart_config)

                        if language == 'es':
                            additional_info = info_client.translate(additional_info)

                        chart_config["additional_info"] = additional_info
                        column_graphs.append(chart_config)

                graphs_output[f"{table_name}.{col}"] = column_graphs

        return graphs_output
