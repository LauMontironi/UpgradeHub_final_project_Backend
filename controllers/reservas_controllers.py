from fastapi import BackgroundTasks, HTTPException
import aiomysql as aio
from db.config import get_conexion
from models.reserva_model import ReservaCreate, ReservaReview
from services.email_service import enviar_confirmacion_reserva


# async def create_reserva(reserva: ReservaCreate, user, background_tasks: BackgroundTasks):
#     conn = None
#     try:
#         conn = await get_conexion()
#         async with conn.cursor(aio.DictCursor) as cursor:
            
#             # 1. Validar disponibilidad
#             await cursor.execute(
#                 """
#                 SELECT id FROM reservas 
#                 WHERE mesa_id=%s AND fecha=%s AND hora=%s AND estado='confirmada'
#                 """,
#                 (reserva.mesa_id, reserva.fecha, reserva.hora)
#             )
#             existing = await cursor.fetchone()
#             if existing:
#                 raise HTTPException(status_code=400, detail="Esa mesa ya está reservada para esa fecha y hora")

#             # 2. Insertar con todas las columnas
#             await cursor.execute(
#                 """
#                 INSERT INTO reservas (usuario_id, mesa_id, fecha, hora, party_size, estado, resena)
#                 VALUES (%s, %s, %s, %s, %s, 'confirmada', %s)
#                 """,
#                 (user["id"], reserva.mesa_id, reserva.fecha, reserva.hora, reserva.party_size, reserva.resena)
#             )
#             await conn.commit()
#             new_id = cursor.lastrowid

#             # 3. Recuperar la reserva creada
#             await cursor.execute("SELECT * FROM reservas WHERE id=%s", (new_id,))
#             item = await cursor.fetchone()

#             # 4. ENVIAR EMAIL EN SEGUNDO PLANO
#             # Usamos los datos del 'user' (que vienen del token) y el 'item' recién creado
#             if user.get("email"):
#                 background_tasks.add_task(
#                     enviar_confirmacion_reserva, 
#                     user["email"], 
#                     item
#                 )

#         return {"msg": "reserva creada correctamente", "item": item}

#     except HTTPException as he:
#         raise he
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
#     finally:
#         if conn:
#             conn.close()

async def create_reserva(reserva: ReservaCreate, user, background_tasks: BackgroundTasks):
    conn = None
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            # 1. Validar disponibilidad
            await cursor.execute(
                """
                SELECT id FROM reservas 
                WHERE mesa_id=%s AND fecha=%s AND hora=%s AND estado='confirmada'
                """,
                (reserva.mesa_id, reserva.fecha, reserva.hora)
            )
            existing = await cursor.fetchone()
            if existing:
                raise HTTPException(status_code=400, detail="Esa mesa ya está reservada")

            # 2. Insertar reserva
            await cursor.execute(
                """
                INSERT INTO reservas (usuario_id, mesa_id, fecha, hora, party_size, estado, resena)
                VALUES (%s, %s, %s, %s, %s, 'confirmada', %s)
                """,
                (user["id"], reserva.mesa_id, reserva.fecha, reserva.hora, reserva.party_size, reserva.resena)
            )
            await conn.commit()
            new_id = cursor.lastrowid

            # 3. Recuperar datos para el email
            await cursor.execute("SELECT * FROM reservas WHERE id=%s", (new_id,))
            item = await cursor.fetchone()

            # 4. Plan B: Asegurar el email si no viene en el token
            email_destino = user.get("email")
            if not email_destino:
                await cursor.execute("SELECT email FROM usuarios WHERE id = %s", (user["id"],))
                res_user = await cursor.fetchone()
                if res_user:
                    email_destino = res_user["email"]

            # 5. Lanzar email si tenemos destinatario
            if email_destino:
                print("📩 Enviando email EN EL REQUEST para:", email_destino)
                background_tasks.add_task(enviar_confirmacion_reserva, email_destino, item)
                print("✅ Terminó la función enviar_confirmacion_reserva()")
            else:
                print("⚠️ No se encontró email para el usuario:", user["id"])


        return {"msg": "reserva creada correctamente", "item": item}

    except HTTPException as he:
        # Esto captura los errores 400 que lanzamos nosotros
        raise he
    except Exception as e:
        # Esto captura errores inesperados
        if conn:
            await conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
    finally:
        # Esto asegura que la conexión siempre se cierre
        if conn:
            conn.close()



async def get_my_reservas(user):
    conn = None
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                "SELECT * FROM reservas WHERE usuario_id=%s ORDER BY fecha DESC, hora DESC",
                (user["id"],)
            )
            return await cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()

async def delete_reserva(reserva_id: int, user):
    conn = None
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            # Primero verificar si la reserva existe
            await cursor.execute("SELECT usuario_id FROM reservas WHERE id=%s", (reserva_id,))
            reserva = await cursor.fetchone()
            
            if not reserva:
                raise HTTPException(status_code=404, detail="Reserva no encontrada")

            # Solo el dueño de la reserva o un administrador pueden borrarla
            if reserva["usuario_id"] != user["id"] and user["rol"] != "admin":
                raise HTTPException(status_code=403, detail="No tienes permisos para eliminar esta reserva")

            # Ejecutar el borrado real en la base de datos
            await cursor.execute("DELETE FROM reservas WHERE id=%s", (reserva_id,))
            await conn.commit()

        return {"msg": "Reserva eliminada definitivamente de la base de datos"}
    
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()

async def add_review(reserva_id: int, reserva_review: ReservaReview, user):
    conn = None
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute("SELECT * FROM reservas WHERE id=%s", (reserva_id,))
            reserva = await cursor.fetchone()
            
            if not reserva:
                raise HTTPException(status_code=404, detail="Reserva no encontrada")

            if reserva["usuario_id"] != user["id"]:
                raise HTTPException(status_code=403, detail="Solo el dueño puede dejar reseña")

            await cursor.execute(
                "UPDATE reservas SET resena=%s WHERE id=%s",
                (reserva_review.resena, reserva_id)
            )
            await conn.commit()

        return {"msg": "reseña guardada correctamente"}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()

async def get_all_reservas():
    conn = None
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute("SELECT * FROM reservas ORDER BY fecha DESC, hora DESC")
            return await cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()