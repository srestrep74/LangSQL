from fastapi import APIRouter, Depends
from src.config.dependencies import get_lang_to_sql_service
from src.modules.text_to_sql.service import LangToSqlService

router = APIRouter()


@router.post("/proccess_query")
def proccess_query(user_input: str, lang_to_sql_service: LangToSqlService = Depends(get_lang_to_sql_service)):
    results = lang_to_sql_service.process_user_query(user_input)
    return {"results": results}