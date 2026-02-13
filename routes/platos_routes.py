from fastapi import APIRouter, Depends
from controllers import plaatos_controller
from core.dependences import is_admin
from models.plato_model import PlatoCreate, PlatoUpdate



router = APIRouter()

@router.get("/platos", status_code=200)
async def get_platos():
    return await plaatos_controller.get_platos()    


@router.post("/", status_code=201)
async def create_plato(plato: PlatoCreate, admin=Depends(is_admin)):
    return await plaatos_controller.create_plato(plato)

@router.put("/{plato_id}", status_code=200)
async def update_plato(plato_id: str, plato: PlatoUpdate, admin=Depends(is_admin)):
    return await plaatos_controller.update_plato(int(plato_id), plato)

@router.delete("/{plato_id}", status_code=200)
async def delete_plato(plato_id: str, admin=Depends(is_admin)):
    return await plaatos_controller.delete_plato(int(plato_id))

@router.get("/{plato_id}", status_code=200)
async def get_plato(plato_id: str):
    return await plaatos_controller.get_plato_by_id(int(plato_id))
