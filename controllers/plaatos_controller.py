from fastapi import HTTPException
import aiomysql as aio
from db.config import get_conexion
from models.plato_model import PlatoCreate, PlatoUpdate


async def get_platos():
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute("""
                        SELECT id, categoria, nombre, descripcion, precio,
                            ingredientes, alergenos, info_nutricional,
                            imagen_url, activo
                        FROM platos
                        WHERE activo = TRUE
                        ORDER BY categoria, nombre
                    """)
            platos = await cursor.fetchall()
            return platos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
            conn.close()

async def create_plato(plato:PlatoCreate):
   
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            query = """
                INSERT INTO platos (categoria, nombre, descripcion, precio, ingredientes, alergenos, info_nutricional, imagen_url, activo)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                plato.categoria, plato.nombre, plato.descripcion, 
                plato.precio, plato.ingredientes, plato.alergenos, 
                plato.info_nutricional, plato.imagen_url, True
            )
            await cursor.execute(query, params)
            await conn.commit()
            return {"msg": "Plato creado con éxito", "id": cursor.lastrowid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear: {str(e)}")
    finally:
        conn.close()

async def update_plato(plato_id, plato:PlatoUpdate):
    
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            # Creamos una actualización dinámica (solo lo que envíes)
            query = """
                UPDATE platos 
                SET categoria=%s, nombre=%s, descripcion=%s, precio=%s, 
                    ingredientes=%s, alergenos=%s, info_nutricional=%s, imagen_url=%s
                WHERE id=%s
            """
            params = (
                plato.categoria, plato.nombre, plato.descripcion, plato.precio,
                plato.ingredientes, plato.alergenos, plato.info_nutricional, 
                plato.imagen_url, plato_id
            )
            await cursor.execute(query, params)
            await conn.commit()
            return {"msg": "Plato actualizado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar: {str(e)}")
    finally:
        conn.close()


async def delete_plato(plato_id):
    
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            # En lugar de borrar, solemos desactivar (Soft Delete)
            await cursor.execute("UPDATE platos SET activo = FALSE WHERE id = %s", (plato_id,))
            await conn.commit()
            return {"msg": "Plato desactivado/eliminado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar: {str(e)}")
    finally:
        conn.close()


async def get_plato_by_id(plato_id: int):
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            # Ejecutamos la consulta para un solo plato
            await cursor.execute("SELECT * FROM platos WHERE id = %s", (plato_id,))
            plato = await cursor.fetchone() # Traemos solo un resultado

            if not plato:
                raise HTTPException(status_code=404, detail="El plato no existe")
            
            return plato
            
    except Exception as e:
        # Si ya es una HTTPException (como el 404), la relanzamos
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        conn.close()