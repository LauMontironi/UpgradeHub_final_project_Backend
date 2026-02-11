from fastapi import APIRouter, Depends
from controllers import resenas_controller
from core.dependences import get_current_user, is_admin
from models.resena_model import ResenaCreate

router = APIRouter()    

@router.post("/", status_code=201)
async def create_resena(resena: ResenaCreate, token_data=Depends(get_current_user)):
    # Aquí usamos el ID del usuario que viene del token
    return await resenas_controller.create_resena(resena, int(token_data.id))

@router.get("/", status_code=200)
async def get_resenas(admin=Depends(is_admin)):
    return await resenas_controller.get_all_resenas()