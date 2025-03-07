from pydantic import BaseModel


class GenerateSyntheticDataRequest(BaseModel):
    schema_name: str
    iterations: int
