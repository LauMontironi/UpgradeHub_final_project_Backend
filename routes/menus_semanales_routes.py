from fastapi import APIRouter, Depends

from controllers import menus_semanales_controller


router = APIRouter()

@router.get("/", status_code=200)
async def get_menus_semanales():
    return await menus_semanales_controller.get_menus_semanales()




# ✅ Menú semanal por ID + sus 3 platos (entrante/principal/postre

@router.get("/{menu_id}", status_code=200)
async def get_menu_semanal(menu_id: str):
    return await menus_semanales_controller.get_menu_semanal(int(menu_id))