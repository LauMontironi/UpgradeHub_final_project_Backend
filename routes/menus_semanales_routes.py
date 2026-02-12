from fastapi import APIRouter, Depends, HTTPException
from controllers import menus_semanales_controller
from core.dependences import is_admin, get_current_user
from models.menu_semanal_model import MenuSemanalCreate, MenuSemanalUpdate

router = APIRouter()

# 1. LISTAR TODOS (Público - Home)
@router.get("/", status_code=200)
async def get_menus_semanales():
    return await menus_semanales_controller.get_menus_semanales()

# 2. VER POR FECHA (Público - Para el filtro de la Home)
@router.get("/fecha/{fecha}", status_code=200)
async def get_menu_by_fecha(fecha: str):
    return await menus_semanales_controller.get_menu_by_fecha(fecha)

# 3. VER DETALLE + PLATOS (Público - Al clicar en la card)
@router.get("/{menu_id}", status_code=200)
async def get_menu_semanal(menu_id: str):
    # Convertimos str a int manualmente como pide el profe
    return await menus_semanales_controller.get_menu_semanal(int(menu_id))

# --- RUTAS DE ADMINISTRADOR (DASHBOARD) ---

# 4. CREAR NUEVO MENÚ (Admin)
@router.post("", status_code=201)
async def create_menu_semanal(menu: MenuSemanalCreate, admin=Depends(is_admin)):
    return await menus_semanales_controller.create_menu_semanal(menu)

# 5. ACTUALIZAR MENÚ (Admin)
@router.put("/{menu_id}", status_code=200)
async def update_menu_semanal(menu_id: str, menu: MenuSemanalUpdate, admin=Depends(is_admin)):
    return await menus_semanales_controller.update_menu_semanal(int(menu_id), menu)

# 6. ELIMINAR MENÚ (Admin)
@router.delete("/{menu_id}", status_code=200)
async def delete_menu_semanal(menu_id: str, admin=Depends(is_admin)):
    return await menus_semanales_controller.delete_menu_semanal(int(menu_id))


# ASIGNAR PLATO A MENÚ (Solo Admin)
# En menus_semanales_routes.py

# ASIGNAR PLATO A MENÚ (Admin)
@router.post("/vincular-plato", status_code=201)
async def asignar_plato(datos: dict, admin=Depends(is_admin)):
    # Sacamos los datos del objeto que manda el Service de Angular
    menu_id = datos.get("menu_id")
    plato_id = datos.get("plato_id")
    rol = datos.get("rol")
    
    # Validamos que no falte nada antes de llamar al controlador
    if menu_id is None or plato_id is None or rol is None:
        raise HTTPException(status_code=400, detail="Faltan datos: menu_id, plato_id o rol")

    # Llamamos a tu controlador convirtiendo a int (como pide el profe)
    return await menus_semanales_controller.asignar_plato_a_menu(
        int(menu_id), 
        int(plato_id), 
        rol
    )

@router.delete("/desvincular-plato/{menu_id}/{plato_id}", status_code=200)
async def desvincular(menu_id: str, plato_id: str, admin=Depends(is_admin)):
    return await menus_semanales_controller.quitar_plato_de_menu(
        int(menu_id), 
        int(plato_id)
    )