import os
import ssl
import aiomysql
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

async def get_conexion():
    # Ruta por defecto al pem dentro del repo
    base_dir = Path(__file__).resolve().parent  # carpeta db/
    ca_default = base_dir / "aiven-ca.pem"

    ca_env = os.getenv("MYSQL_CA_CERT")
    ca_path = Path(ca_env) if ca_env else ca_default

    # ✅ Si el archivo no existe, NO fallar: usar CAs del sistema
    if ca_path.exists():
        ssl_context = ssl.create_default_context(cafile=str(ca_path))
    else:
        ssl_context = ssl.create_default_context()

    return await aiomysql.connect(
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT")),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        db=os.getenv("MYSQL_DATABASE"),
        autocommit=True,
        ssl=ssl_context,
    )
