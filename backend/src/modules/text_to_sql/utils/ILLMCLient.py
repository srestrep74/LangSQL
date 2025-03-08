from abc import ABC, abstractmethod

class ILLMClient(ABC):
    @abstractmethod
    def get_model_response(self, db_structure: str, user_input: str) -> str:
        ...