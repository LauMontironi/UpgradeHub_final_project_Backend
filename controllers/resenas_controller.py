from datetime import datetime
from fastapi import HTTPException
import aiomysql as aio
from db.config import get_conexion

async def create_resena(resena, usuario_id: int):
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:

            ahora = datetime.now().strftime('%Y-%m-%d')
            
            await cursor.execute(
                """SELECT id FROM reservas 
                   WHERE usuario_id = %s AND fecha < %s 
                   LIMIT 1""", 
                (usuario_id, ahora)
            )
            reserva_pasada = await cursor.fetchone()

            if not reserva_pasada:
                raise HTTPException(status_code=404, detail="Solo puedes escribir una reseña si has disfrutado de una reserva anteriormente.")
            
            await cursor.execute(
                "INSERT INTO resenas (usuario_id, comentario, puntuacion, fecha) VALUES (%s, %s, %s, %s)",
                (usuario_id, resena.comentario, resena.puntuacion, resena.fecha)
            )
            await conn.commit()
            return {"msg": "Reseña enviada, ¡gracias por tu visita!"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()

async def get_all_resenas():
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute("SELECT r.*, u.nombre FROM resenas r JOIN usuarios u ON r.usuario_id = u.id ORDER BY r.fecha DESC")
            resenas = await cursor.fetchall()
            return resenas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()

async def get_resenas_por_usuario(usuario_id: int):
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute("SELECT * FROM resenas WHERE usuario_id = %s ORDER BY fecha DESC", (usuario_id,))
            return await cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()