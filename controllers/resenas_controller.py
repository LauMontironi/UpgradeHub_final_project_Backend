from datetime import datetime
from fastapi import HTTPException
import aiomysql as aio
from db.config import get_conexion

async def create_resena(resena, usuario_id: int):
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:

            ahora = datetime.now().strftime('%Y-%m-%d')
            
            # 1. Validamos que la reserva exista, sea del usuario, sea pasada Y NO tenga reseña ya
            await cursor.execute(
                """SELECT id FROM reservas 
                   WHERE id = %s AND usuario_id = %s AND fecha <= %s""", 
                (resena.reserva_id, usuario_id, ahora)
            )
            reserva_valida = await cursor.fetchone()

            if not reserva_valida:
                raise HTTPException(
                    status_code=400, 
                    detail="No puedes comentar esta reserva (puede que sea futura o no te pertenezca)."
                )

            # 2. Comprobar si ya existe una reseña para esta reserva específica
            await cursor.execute("SELECT id FROM resenas WHERE reserva_id = %s", (resena.reserva_id,))
            existe = await cursor.fetchone()
            if existe:
                raise HTTPException(status_code=400, detail="Ya has escrito una reseña para esta visita.")
            
            # 3. Insertar con el reserva_id asociado
            await cursor.execute(
                """INSERT INTO resenas (usuario_id, reserva_id, comentario, puntuacion, fecha) 
                   VALUES (%s, %s, %s, %s, %s)""",
                (usuario_id, resena.reserva_id, resena.comentario, resena.puntuacion, resena.fecha)
            )
            
            await conn.commit()
            return {"msg": "Reseña enviada, ¡gracias por tu visita!"}
        
    except HTTPException as he:
        raise he
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
    conn = await get_conexion()
    try:
        async with conn.cursor(aio.DictCursor) as cursor:
            query = """
                SELECT
                    id,
                    reserva_id,
                    usuario_id,
                    comentario,
                    puntuacion,
                    fecha
                FROM resenas
                WHERE usuario_id = %s
                ORDER BY fecha DESC
            """
            await cursor.execute(query, (usuario_id,))
            return await cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


async def update_resena(resena_id: int, resena_data, usuario_id: int):
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            # 1. Verificamos que la reseña existe y pertenece al usuario
            await cursor.execute(
                "SELECT id FROM resenas WHERE id = %s AND usuario_id = %s",
                (resena_id, usuario_id)
            )
            existe = await cursor.fetchone()
            
            if not existe:
                raise HTTPException(
                    status_code=404, 
                    detail="Reseña no encontrada o no tienes permiso para editarla."
                )

            # 2. Actualizamos el comentario, la puntuación y la fecha de edición
            ahora = datetime.now().strftime('%Y-%m-%d')
            await cursor.execute(
                """UPDATE resenas 
                   SET comentario = %s, puntuacion = %s, fecha = %s 
                   WHERE id = %s""",
                (resena_data.comentario, resena_data.puntuacion, ahora, resena_id)
            )
            
            await conn.commit()
            return {"msg": "Reseña actualizada correctamente"}
            
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar: {str(e)}")
    finally:
        conn.close()