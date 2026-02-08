from fastapi import FastAPI
from routes  import mesas_routes, test_db_routes, auth_routes, usuarios_routes, reservas_routes, menu_routes, platos_routes, menus_semanales_routes

import os





app = FastAPI()



# 1. Recuperamos el contenido de la variable que pegaste en Railway
ca_content = os.getenv("MYSQL_CA_CONTENT")

# 2. Definimos dónde queremos que se guarde el archivo temporalmente
# Usaremos '/app/aiven-ca.pem' que es una ruta segura en Railway
ca_path = "/app/aiven-ca.pem"

if ca_content:
    with open(ca_path, "w") as f:
        f.write(ca_content)
    # 3. Actualizamos la variable de entorno para que el resto del código
    # use esta nueva ruta de archivo que acabamos de crear
    os.environ["MYSQL_CA_CERT"] = ca_path




app.include_router(test_db_routes.router, prefix="/debug", tags=["debug"])

app.include_router(auth_routes.router, prefix='/auth', tags= ['auth'])

app.include_router(usuarios_routes.router, prefix='/usuarios', tags= ['usuarios'])


app.include_router(menu_routes.router, prefix='/menu', tags= ['menu'])


app.include_router(reservas_routes.router, prefix="/reservas", tags=["reservas"])

app.include_router(mesas_routes.router, prefix="/mesas", tags=["mesas"])

app.include_router(platos_routes.router, prefix="/platos", tags=["platos"])

app.include_router(menus_semanales_routes.router, prefix="/menus-semanales", tags=["menus-semanales"])