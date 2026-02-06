from fastapi import HTTPException
import aiomysql as aio
from db.config import get_conexion
from models.reserva_model import ReservaCreate, ReservaReview

async def create_reserva(reserva:ReservaCreate, user):
   
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            # 🚫 validar que no exista reserva confirmada para esa mesa y esa fecha
            await cursor.execute(
                """
                SELECT id FROM reservas
                WHERE mesa_id=%s AND fecha_reserva=%s AND estado='confirmada'
                """,
                (reserva.mesa_id, reserva.fecha_reserva)
            )
            existing = await cursor.fetchone()
            if existing:
                raise HTTPException(status_code=400, detail="Esa mesa ya está reservada para esa fecha")

            await cursor.execute(
                """
                INSERT INTO reservas (usuario_id, mesa_id, fecha_reserva, estado, resena)
                VALUES (%s, %s, %s, 'confirmada', NULL)
                """,
                (user["id"], reserva.mesa_id, reserva.fecha_reserva)
            )
            await conn.commit()
            new_id = cursor.lastrowid

            await cursor.execute("SELECT * FROM reservas WHERE id=%s", (new_id,))
            item = await cursor.fetchone()

        return {"msg": "reserva creada correctamente", "item": item}


    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
    
            conn.close()

async def get_my_reservas(user):
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                "SELECT * FROM reservas WHERE usuario_id=%s ORDER BY fecha_reserva DESC",
                (user["id"],)
            )
            return await cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
            conn.close()

async def cancel_reserva(reserva_id: int, user):
    
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            # asegurar que la reserva sea del usuario
            await cursor.execute("SELECT * FROM reservas WHERE id=%s", (reserva_id,))
            reserva = await cursor.fetchone()
            if not reserva:
                raise HTTPException(status_code=404, detail="Reserva no encontrada")

            if reserva["usuario_id"] != user["id"] and user["rol"] != "admin":
                raise HTTPException(status_code=403, detail="No tienes permisos para cancelar esta reserva")

            await cursor.execute(
                "UPDATE reservas SET estado='cancelada' WHERE id=%s",
                (reserva_id,)
            )
            await conn.commit()

        return {"msg": "reserva cancelada correctamente"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
    
            conn.close()

async def add_review(reserva_id: int, reserva:ReservaReview, user):

    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute("SELECT * FROM reservas WHERE id=%s", (reserva_id,))
            reserva = await cursor.fetchone()
            if not reserva:
                raise HTTPException(status_code=404, detail="Reserva no encontrada")

            if reserva["usuario_id"] != user["id"]:
                raise HTTPException(status_code=403, detail="Solo el dueño de la reserva puede dejar reseña")

            await cursor.execute(
                "UPDATE reservas SET resena=%s WHERE id=%s",
                (reserva.resena, reserva_id)
            )
            await conn.commit()

        return {"msg": "reseña guardada correctamente"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
            conn.close()

async def get_all_reservas():
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute("SELECT * FROM reservas ORDER BY fecha_reserva DESC")
            return await cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
            conn.close()
