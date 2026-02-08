from fastapi import APIRouter, HTTPException 
import aiomysql as aio
from core.security import create_token, hash_password, verify_password
from db.config import get_conexion

router = APIRouter()

# 🔍 GET /usuarios/id

async def get_user_id(usuario_id: int):
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                """
                SELECT id, nombre, apellido, email, telefono, edad, alergias, rol
                FROM usuarios
                WHERE id = %s
                """,
                (usuario_id,)
            )
            user= await cursor.fetchone()
            return user


    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()