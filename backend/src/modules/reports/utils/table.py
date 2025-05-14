import pandas as pd

from .base_graph import BaseGraph


class Table(BaseGraph):
    def generate(self, column: str, df: pd.DataFrame) -> dict:
        if column == "*":
            data_subset = df
        else:
            cols = [col.strip() for col in column.split(",")]
            data_subset = df[cols]

        return {
            "type": "table",
            "data": {
                "columns": list(data_subset.columns),
                "rows": data_subset.head(100).fillna("").values.tolist()
            }
        }
