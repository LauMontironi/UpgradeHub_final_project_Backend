from fastapi import HTTPException
import aiomysql as aio
from db.config import get_conexion


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

