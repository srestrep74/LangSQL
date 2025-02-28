from fastapi import APIRouter, Depends, status

from src.config.dependencies import get_lang_to_sql_service
from src.modules.text_to_sql.schemas.ProcessQueryRequest import ProcessQueryRequest
from src.modules.text_to_sql.service import LangToSqlService
from src.utils.ResponseManager import ResponseManager

router = APIRouter()


@router.post("/proccess_query")
def proccess_query(
    request: ProcessQueryRequest, lang_to_sql_service: LangToSqlService = Depends(get_lang_to_sql_service)
):
    try:
        results = lang_to_sql_service.process_user_query(request.user_input)
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