from abc import ABC, abstractmethod
import pandas as pd


class BaseGraph(ABC):
    @abstractmethod
    def generate(self, column: str, df: pd.DataFrame) -> dict:
        pass
