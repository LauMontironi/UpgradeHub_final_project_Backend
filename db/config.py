import os
import ssl
import aiomysql
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

async def get_conexion():
    # Ruta absoluta al certificado dentro del proyecto
    base_dir = Path(__file__).resolve().parent  # .../db
    ca_default = base_dir / "aiven-ca.pem"

    ca_path_env = os.getenv("MYSQL_CA_CERT")
    ca_path = Path(ca_path_env) if ca_path_env else ca_default

    ssl_context = ssl.create_default_context(cafile=str(ca_path))
    
    return await aiomysql.connect(
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT")),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        db=os.getenv("MYSQL_DATABASE"),
        autocommit=True,
        ssl=ssl_context,
    )
