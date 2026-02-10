from fastapi import HTTPException
import aiomysql as aio
from db.config import get_conexion
from models.menu_semanal_model import MenuSemanalCreate, MenuSemanalUpdate


async def get_menus_semanales():
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute("""
            SELECT * FROM menus_semanales ORDER BY fecha DESC
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
            # 1) Traer la información básica del menú de la tabla menus_semanales
            await cursor.execute("""
                SELECT id, numero, titulo, descripcion, precio, activo, fecha 
                FROM menus_semanales 
                WHERE id = %s
            """, (menu_id,))
            
            menu_encontrado = await cursor.fetchone()

            if not menu_encontrado:
                return {"detail": "Menú semanal no encontrado"}

            # 2) Traer los platos asociados a este menú
            # Unimos la tabla puente (menu_semanal_platos) con la de platos
            await cursor.execute("""
                SELECT 
                    menu_semanal_platos.rol,
                    platos.id, 
                    platos.categoria, 
                    platos.nombre, 
                    platos.descripcion, 
                    platos.precio,
                    platos.ingredientes, 
                    platos.alergenos, 
                    platos.info_nutricional,
                    platos.imagen_url, 
                    platos.activo
                FROM menu_semanal_platos
                INNER JOIN platos ON platos.id = menu_semanal_platos.plato_id
                WHERE menu_semanal_platos.menu_id = %s
                ORDER BY FIELD(menu_semanal_platos.rol, 'entrante', 'principal', 'postre')
            """, (menu_id,))
            
            lista_de_platos = await cursor.fetchall()

        # 3) Devolvemos un objeto con toda la información unificada
        return {
            "menu": menu_encontrado,
            "platos": lista_de_platos
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        if conn:
            conn.close()


async def create_menu_semanal(menu: MenuSemanalCreate):
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                """INSERT INTO menus_semanales (numero, titulo, descripcion, precio, activo, fecha) 
                VALUES (%s, %s, %s, %s, %s, %s)""",
                (menu.numero, menu.titulo, menu.descripcion, menu.precio, menu.activo, menu.fecha)
            )
            await conn.commit()
            return {"msg": "Menú creado correctamente", "id": cursor.lastrowid}
    finally:
        conn.close()

# Para la Home: obtener el menú de una fecha específica
async def get_menu_by_fecha(fecha: str):
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute("SELECT * FROM menus_semanales WHERE fecha = %s AND activo = TRUE", (fecha,))
            return await cursor.fetchone()
    finally:
        conn.close()

# ACTUALIZAR (Admin - Dashboard)
async def update_menu_semanal(menu_id: int, menu: MenuSemanalUpdate):
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                """UPDATE menus_semanales SET titulo=%s, descripcion=%s, precio=%s, activo=%s, fecha=%s 
                WHERE id=%s""",
                (menu.titulo, menu.descripcion, menu.precio, menu.activo, menu.fecha, menu_id)
            )
            await conn.commit()
            return {"msg": "Menú actualizado"}
    finally:
        conn.close()

# 5. ELIMINAR (Admin - Dashboard)
async def delete_menu_semanal(menu_id: int):
    try:
        conn = await get_conexion()
        async with conn.cursor() as cursor:
            await cursor.execute("DELETE FROM menus_semanales WHERE id=%s", (menu_id,))
            await conn.commit()
            return {"msg": "Menú eliminado correctamente"}
    finally:
        conn.close()




async def asignar_plato_a_menu(menu_id: int, plato_id: int, rol: str):
    conn = None
    try:
        conn = await get_conexion()
        async with conn.cursor() as cursor:
            # Insertamos en la tabla puente
            await cursor.execute(
                """
                INSERT INTO menu_semanal_platos (menu_id, plato_id, rol)
                VALUES (%s, %s, %s)
                """,
                (menu_id, plato_id, rol)
            )
            await conn.commit()
            return {"msg": f"Plato asignado como {rol} correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al asignar plato: {str(e)}")
    finally:
        if conn:
            conn.close()