import pandas as pd

from .bar_chart import BarChart
from .pie_chart import PieChart
from .table import Table
from .histogram import Histogram

GRAPH_SUGGESTIONS = {
    "categorical": [BarChart, PieChart, Table],
    "numerical": [Histogram, BarChart],
    "datetime": [BarChart],
}

class GraphFactory:
    @staticmethod
    def get_graphs(column_type: str):
        return GRAPH_SUGGESTIONS.get(column_type, [])
