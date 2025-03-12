from pydantic import BaseModel


class ProcessQueryRequest(BaseModel):
    user_input: str
    schema_name: str
