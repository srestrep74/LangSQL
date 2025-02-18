from fastapi import APIRouter

router = APIRouter()

@router.post("/alive")
async def alive():
    return {"message": "control_panel Working"}
