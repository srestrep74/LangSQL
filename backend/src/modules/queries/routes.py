from fastapi import APIRouter, Depends
from src.config.dependencies import get_query_service
from src.modules.queries.service import QueryService

import urllib.parse

router = APIRouter()


@router.get("/db_structure/")
async def get_db_structure(query_service: QueryService = Depends(get_query_service)):
    structure = await query_service.get_db_structure()
    return {"structure": structure}


@router.post("/execute_query/")
async def execute_query(query: str, query_service: QueryService = Depends(get_query_service)):
    query = urllib.parse.unquote(query)
    results = await query_service.execute_query(query)
    return {"results": results}
