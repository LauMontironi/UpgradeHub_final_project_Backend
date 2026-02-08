from fastapi import APIRouter, Depends
from controllers import plaatos_controller



router = APIRouter()

@router.get("/platos", status_code=200)
async def get_platos():
    return await plaatos_controller.get_platos()    