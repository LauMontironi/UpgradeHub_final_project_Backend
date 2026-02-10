from fastapi import APIRouter, Depends
from core.dependences import get_current_user, is_admin
from controllers import reservas_controllers
from models.reserva_model import ReservaCreate, ReservaReview

router = APIRouter()

@router.post("", status_code=201)
async def create_reserva(reserva: ReservaCreate, user=Depends(get_current_user)):
    return await reservas_controllers.create_reserva(reserva, user)

@router.get("/me", status_code=200)
async def get_my_reservas(user=Depends(get_current_user)):
    return await reservas_controllers.get_my_reservas(user)

@router.delete("/{reserva_id}", status_code=200)
async def delete_reserva(reserva_id: str, user=Depends(get_current_user)):
    return await reservas_controllers.delete_reserva(int(reserva_id), user)


# RUTA PARA RESEÑA (PATCH)
@router.patch("/{reserva_id}/review", status_code=200)
async def add_review(reserva_id: str, reserva: ReservaReview, user=Depends(get_current_user)):
    return await reservas_controllers.add_review(int(reserva_id), reserva, user)

# RUTA PARA VER TODAS (GET - SOLO ADMIN)
@router.get("", status_code=200)
async def get_all_reservas(admin=Depends(is_admin)):
    return await reservas_controllers.get_all_reservas()
