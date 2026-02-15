from fastapi import APIRouter, Depends
from core.dependences import is_admin_or_owner
from controllers import usuarios_controllers
from models.usuario_model import UsuarioPasswordUpdate, UsuarioUpdate  

router = APIRouter()

# 🔍 GET /usuarios/id


@router.get("/{user_id}", status_code=200)
async def get_user_id(user_id: str, current_user=Depends(is_admin_or_owner)):
    return await usuarios_controllers.get_user_id(int(user_id))



# PUT /usuarios/id

@router.put("/{user_id}", status_code=200)
async def update_user(user_id: str, data: UsuarioUpdate, current_user=Depends(is_admin_or_owner)):
    return await usuarios_controllers.update_user(int(user_id), data)


@router.put("/{user_id}/password", status_code=200)
async def change_password(
    user_id: str,
    data: UsuarioPasswordUpdate,
    current_user=Depends(is_admin_or_owner)
):
    return await usuarios_controllers.update_password(int(user_id), data, current_user)