from fastapi import HTTPException
import aiomysql as aio
from db.config import get_conexion


async def get_menus_semanales():
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute("""
            SELECT id, numero, titulo, descripcion, precio, activo
            FROM menus_semanales
            WHERE activo = TRUE
            ORDER BY numero
        """)
        rows = await cursor.fetchall()
        return rows
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:                
        conn.close()


async def get_menu_semanal(menu_id: int):
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            # 1) traer el menú
            await cursor.execute("""
                SELECT id, numero, titulo, descripcion, precio, activo
                FROM menus_semanales
                WHERE id = %s
            """, (menu_id,))
            menu = await cursor.fetchone()

            if not menu:
                return {"detail": "Menú semanal no encontrado"}

            menu_dict = menu

            # 2) traer platos del menú (con toda la info)
            await cursor.execute("""
                SELECT msp.rol,
                       p.id, p.categoria, p.nombre, p.descripcion, p.precio,
                       p.ingredientes, p.alergenos, p.info_nutricional,
                       p.imagen_url, p.activo
                FROM menu_semanal_platos msp
                JOIN platos p ON p.id = msp.plato_id
                WHERE msp.menu_id = %s
                ORDER BY FIELD(msp.rol, 'entrante', 'principal', 'postre')
            """, (menu_id,))
            platos = await cursor.fetchall()

        platos_list = platos

        return {
            "menu": menu_dict,
            "platos": platos_list
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()
