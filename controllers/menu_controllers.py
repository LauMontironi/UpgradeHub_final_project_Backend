from datetime import datetime
from fastapi import HTTPException 
import aiomysql as aio
from db.config import get_conexion
from models.menu_model import MenuCreate, MenuUpdate



# get all menues 
async def get_menus():
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute("SELECT * FROM menus")
            menus = await cursor.fetchall()
            return menus
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()

# get menu by fecha

async def get_menus_by_fecha(fecha: str):
    conn = None
    try:
        # Validar formato YYYY-MM-DD
        try:
            fecha_valida = datetime.strptime(fecha, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato de fecha inválido. Usa YYYY-MM-DD")

        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute("SELECT * FROM menus WHERE fecha = %s", (fecha_valida,))
            menu = await cursor.fetchone()

        if not menu:
            raise HTTPException(status_code=404, detail="No hay menú disponible para esa fecha")

        return {"success": True, "menu": menu}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if conn is not None:
            conn.close()



async def create_menu(menu:MenuCreate):
    
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            
            await cursor.execute(
                """
                INSERT INTO menus (fecha, nombre, descripcion, foto_url, precio)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (menu.fecha, menu.nombre, menu.descripcion, menu.foto_url, menu.precio)
            )
            await conn.commit()
            new_id = cursor.lastrowid

            await cursor.execute("SELECT * FROM menus WHERE id=%s", (new_id,))
            item = await cursor.fetchone()

        return {"msg": "menú creado correctamente", "item": item}

    except Exception as e:
        # si se repite fecha, caerá aquí (puedes refinar luego con error code)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
            conn.close()

async def update_menu(menu_id: int, menu:MenuUpdate):
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                """
                UPDATE menus
                SET nombre=%s, descripcion=%s, foto_url=%s, precio=%s
                WHERE id=%s
                """,
                (menu.nombre, menu.descripcion, menu.foto_url, menu.precio, menu_id)
            )
            await conn.commit()

            await cursor.execute("SELECT * FROM menus WHERE id=%s", (menu_id,))
            item = await cursor.fetchone()

        if not item:
            raise HTTPException(status_code=404, detail="Menú no encontrado")

        return {"msg": "menú actualizado correctamente", "item": item}


    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
            conn.close()

async def delete_menu(menu_id: int):
    try:
        conn = await get_conexion()
        async with conn.cursor() as cursor:
            await cursor.execute("DELETE FROM menus WHERE id=%s", (menu_id,))
            await conn.commit()

        return {"msg": "menú eliminado correctamente"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
            conn.close()

