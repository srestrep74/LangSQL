from pydantic import BaseModel


class ResponseError(BaseModel):
    """
    Data model for API error responses.
    
    The `detail` attribute provides a descriptive message 
    about the specific error.
    """
    detail: str