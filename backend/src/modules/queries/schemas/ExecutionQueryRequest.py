from pydantic import BaseModel

class ExecutionQueryRequest(BaseModel):
    query: str