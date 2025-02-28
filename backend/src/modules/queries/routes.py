import urllib.parse

from fastapi import APIRouter, Depends, status

from src.config.dependencies import get_query_service
from src.modules.queries.schemas.ExecutionQueryRequest import ExecutionQueryRequest
from src.modules.queries.service import QueryService
from src.utils.ResponseManager import ResponseManager

router = APIRouter()


@router.get("/db_structure/")
def get_db_structure(query_service: QueryService = Depends(get_query_service)):
    try:
        db_structure = query_service.get_db_structure()
        return ResponseManager.success_response(
            data={"db_structure": db_structure},
            message="Success",
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        return ResponseManager.error_response(
            message="Error",
            status_code=status.HTTP_400_BAD_REQUEST,
            details={"error": str(e)},
        )


@router.post("/execute_query/")
def execute_query(
    request: ExecutionQueryRequest, query_service: QueryService = Depends(get_query_service)
):
    try:
        query = urllib.parse.unquote(request.query)
        results = query_service.execute_query(query)
        return ResponseManager.success_response(
            data={"results": results},
            message="Success",
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        return ResponseManager.error_response(
            message="Error",
            status_code=status.HTTP_400_BAD_REQUEST,
            details={"error": str(e)},
        )