import aiomysql
import ssl
import os
from dotenv import load_dotenv

load_dotenv()

async def get_conexion():
    # ✅ SSL por defecto (usa CAs del sistema del contenedor)
    ssl_context = ssl.create_default_context()

    return await aiomysql.connect(
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT")),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        db=os.getenv("MYSQL_DATABASE"),
        ssl=ssl_context
    )
