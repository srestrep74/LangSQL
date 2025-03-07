from fastapi import APIRouter, Depends, status

from src.config.dependencies import get_lang_to_sql_service, get_synthetic_data_model_service
from src.modules.text_to_sql.schemas.ProcessQueryRequest import ProcessQueryRequest
from src.modules.text_to_sql.service import LangToSqlService, SyntheticDataModelService
from src.utils.ResponseManager import ResponseManager
from src.modules.text_to_sql.models.models import GenerateSyntheticDataRequest

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


@router.post("/generate_synthetic_data")
async def generate_synthetic_data(
    request: GenerateSyntheticDataRequest,
    synthetic_data_model_service: SyntheticDataModelService = Depends(get_synthetic_data_model_service)
):
    """
    This endpoint generates synthetic data and inserts it into the user database.

    Args:

        synthetic_data_model_service: A service for generating synthetic data. Retrieved via `Depends(get_synthetic_data_model_service)`.

    Returns:

        Successful Response (`200 OK`)
        ```json
        {
            "status": "success",
            "message": "Success",
            "data": {
                "results": [...]
            }
        }
        ```

        Error Response (`400 Bad Request`)
        ```json
        {
            "status": "error",
            "message": "Error",
            "details": {
                "error": "Error description"
            }
        }
        ```
    """
    try:
        schema_name = request.schema_name
        iterations = request.iterations
        results = synthetic_data_model_service.generate_synthetic_data(iterations=iterations, schema_name=schema_name)

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
