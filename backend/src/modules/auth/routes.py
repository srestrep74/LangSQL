from fastapi import APIRouter

router = APIRouter()

@router.post("/alive")
async def alive():
    return {"message": "auth Working"}
