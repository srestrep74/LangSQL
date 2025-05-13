from .base_graph import BaseGraph
import pandas as pd

class BarChart(BaseGraph):
    def generate(self, column: str, df: pd.DataFrame) -> dict:
        data = df[column].value_counts()
        return {
            "type": "bar",
            "data": {
                "labels": list(data.index),
                "datasets": [{
                    "label": column,
                    "data": [int(val) for val in data.values],
                    "backgroundColor": "rgba(75, 192, 192, 0.2)",
                    "borderColor": "rgba(75, 192, 192, 1)",
                    "borderWidth": 1,
                }]
            }
        }
