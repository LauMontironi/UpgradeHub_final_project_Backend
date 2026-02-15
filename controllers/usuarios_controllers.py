from fastapi import APIRouter, HTTPException 
import aiomysql as aio
from core.security import create_token, hash_password, verify_password
from db.config import get_conexion
from models.usuario_model import UsuarioPasswordUpdate, UsuarioUpdate

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

async def update_user(usuario_id: int, data: UsuarioUpdate):
    conn = None
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:

            # 1) Existe?
            await cursor.execute("SELECT id FROM usuarios WHERE id=%s", (usuario_id,))
            user = await cursor.fetchone()
            if not user:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")

            # 2) Update dinámico: solo campos enviados
            fields = []
            values = []

            if data.nombre is not None:
                fields.append("nombre=%s")
                values.append(data.nombre)

            if data.apellido is not None:
                fields.append("apellido=%s")
                values.append(data.apellido)

            if data.telefono is not None:
                fields.append("telefono=%s")
                values.append(data.telefono)

            if data.edad is not None:
                fields.append("edad=%s")
                values.append(data.edad)

            if data.alergias is not None:
                fields.append("alergias=%s")
                values.append(data.alergias)

            if not fields:
                return {"msg": "Nada para actualizar"}

            values.append(usuario_id)

            query = f"UPDATE usuarios SET {', '.join(fields)} WHERE id=%s"
            await cursor.execute(query, tuple(values))
            await conn.commit()

            # 3) Devolvemos el usuario actualizado (sin password)
            await cursor.execute("""
                SELECT id, nombre, apellido, dni, email, telefono, edad, alergias, rol
                FROM usuarios
                WHERE id=%s
            """, (usuario_id,))
            updated = await cursor.fetchone()

            return {"msg": "Usuario actualizado", "user": updated}

    except HTTPException as he:
        raise he
    except Exception as e:
        if conn:
            await conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()


async def update_password(usuario_id: int, data: UsuarioPasswordUpdate, current_user: dict):
    conn = None
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:

            # 1) Traer password hash actual
            await cursor.execute(
                "SELECT id, password FROM usuarios WHERE id=%s",
                (usuario_id,)
            )
            user = await cursor.fetchone()
            if not user:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")

            # 2) Si NO es admin, debe validar current_password
            if current_user.get("rol") != "admin":
                if not verify_password(data.current_password, user["password"]):
                    raise HTTPException(status_code=400, detail="La contraseña actual no es correcta")

            # 3) Hashear nueva password y guardar
            new_hash = hash_password(data.new_password)

            await cursor.execute(
                "UPDATE usuarios SET password=%s WHERE id=%s",
                (new_hash, usuario_id)
            )
            await conn.commit()

            return {"msg": "Contraseña actualizada correctamente"}

    except HTTPException as he:
        raise he
    except Exception as e:
        if conn:
            await conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()