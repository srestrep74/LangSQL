from typing import Dict, Any, Optional
from fastapi import status


class ResponseManager:
    @staticmethod
    def success_response(data: Optional[Dict[str, Any]] = None, message: str = "Success", status_code: int = status.HTTP_200_OK) -> Dict[str, Any]:
        return {
            "status": "success",
            "message": message,
            "data": data,
            "status_code": status_code
        }

    @staticmethod
    def error_response(message: str, status_code: int = status.HTTP_400_BAD_REQUEST, details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return {
            "status": "error",
            "message": message,
            "details": details,
            "status_code": status_code
        }
