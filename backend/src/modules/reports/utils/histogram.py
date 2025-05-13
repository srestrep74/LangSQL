from .base_graph import BaseGraph
import pandas as pd

class Histogram(BaseGraph):
    def generate(self, column: str, df: pd.DataFrame) -> dict:
        data = df[column].dropna()
        counts, bins = pd.cut(data, bins=10, retbins=True)
        bin_labels = [f"{round(bins[i], 2)} - {round(bins[i+1], 2)}" for i in range(len(bins)-1)]
        bin_counts = counts.value_counts(sort=False)
        
        return {
            "type": "bar",
            "data": {
                "labels": bin_labels,
                "datasets": [{
                    "label": f"Histogram of {column}",
                    "data": bin_counts.tolist(),
                    "backgroundColor": "rgba(75, 192, 192, 0.2)",
                    "borderColor": "rgba(75, 192, 192, 1)",
                    "borderWidth": 1,
                }]
            }
        }
