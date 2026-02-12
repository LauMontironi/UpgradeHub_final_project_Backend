from fastapi import HTTPException
import aiomysql as aio
from db.config import get_conexion
from models.mesa_model import MesaCreate, MesaUpdate

async def get_mesas():
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute("SELECT * FROM mesas ORDER BY numero_mesa ASC")
            return await cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
            conn.close()

async def create_mesa(mesa: MesaCreate):
    conn = await get_conexion()
    try:
        async with conn.cursor(aio.DictCursor) as cursor:
        
            if mesa.capacidad <= 0:
                raise HTTPException(status_code=400, detail="La capacidad debe ser mayor a 0")

           
            await cursor.execute("SELECT id FROM mesas WHERE numero_mesa = %s", (mesa.numero_mesa,))
            if await cursor.fetchone():
                raise HTTPException(status_code=400, detail=f"El número de mesa {mesa.numero_mesa} ya está registrado")

    
            await cursor.execute(
                "INSERT INTO mesas (numero_mesa, capacidad) VALUES (%s, %s)",
                (mesa.numero_mesa, mesa.capacidad)
            )
            await conn.commit()
            new_id = cursor.lastrowid

           
            await cursor.execute("SELECT * FROM mesas WHERE id=%s", (new_id,))
            item = await cursor.fetchone()

        return {"msg": "Mesa creada correctamente", "item": item}


    except Exception as e:
        
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
    finally:
        conn.close()

async def update_mesa(mesa_id: int, mesa:MesaUpdate):
   
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                "UPDATE mesas SET numero_mesa=%s, capacidad=%s WHERE id=%s",
                (mesa.numero_mesa, mesa.capacidad, mesa_id)
            )
            await conn.commit()

            await cursor.execute("SELECT * FROM mesas WHERE id=%s", (mesa_id,))
            item = await cursor.fetchone()

        if not item:
            raise HTTPException(status_code=404, detail="Mesa no encontrada")

        return {"msg": "mesa actualizada correctamente", "item": item}
   
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
    
            conn.close()

async def delete_mesa(mesa_id: int):

    try:
        conn = await get_conexion()
        async with conn.cursor() as cursor:
            await cursor.execute("DELETE FROM mesas WHERE id=%s", (mesa_id,))
            await conn.commit()
        return {"msg": "mesa eliminada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
       
            conn.close()
