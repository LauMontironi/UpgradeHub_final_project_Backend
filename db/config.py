import aiomysql
import ssl
import os
from dotenv import load_dotenv

load_dotenv()

async def get_conexion():
    ca_path = os.getenv("MYSQL_CA_CERT", "db/aiven-ca.pem")

    ssl_context = ssl.create_default_context(cafile=ca_path)

    return await aiomysql.connect(
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT")),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        db=os.getenv("MYSQL_DATABASE"),
        ssl=ssl_context 
    )

