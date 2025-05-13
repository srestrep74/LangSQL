from .base_graph import BaseGraph
import pandas as pd


class PieChart(BaseGraph):
    def generate(self, column: str, df: pd.DataFrame) -> dict:
        data = df[column].value_counts()
        return {
            "type": "pie",
            "data": {
                "labels": list(data.index),
                "datasets": [{
                    "label": column,
                    "data": [int(val) for val in data.values],
                    "backgroundColor": [
                        "rgba(255, 99, 132, 0.2)",
                        "rgba(54, 162, 235, 0.2)",
                        "rgba(255, 206, 86, 0.2)",
                    ],
                    "borderColor": [
                        "rgba(255, 99, 132, 1)",
                        "rgba(54, 162, 235, 1)",
                        "rgba(255, 206, 86, 1)",
                    ],
                    "borderWidth": 1,
                }]
            }
        }
