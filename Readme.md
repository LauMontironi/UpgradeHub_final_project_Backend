🍣 UpgradeFood — Documentación Backend Completa

Este backend representa la operativa de un restaurante real:
clientes que consultan menús y reservan, y un administrador que gestiona menús, mesas, carta y revisa actividad.

1️⃣ Creación del entorno de trabajo:

mkdir ProyectoUpgrade
cd ProyectoUpgrade

2️⃣ Entorno virtual y dependencias

Creamos y activamos un entorno virtual para aislar el proyecto:

python -m venv .venv
source .venv/Scripts/activate # Windows Git Bash

Instalamos dependencias:

pip install "fastapi[standard]"
pip install aiomysql
pip install python-dotenv
pip install "passlib[argon2]"
pip install "python-jose[cryptography]"

Guardamos versiones:

pip freeze > requirements.txt

3️⃣ Base de Datos MySQL (Aiven)

Decidimos que la base de datos no debía estar en localhost para que el sistema funcione en producción y para que todos los integrantes del equipo puedan conectarse.

Además:

✔ Las imágenes de los menús NO se guardan en el frontend
✔ Se almacenan en la nube (Cloudflare R2 / similar)
✔ En la base solo guardamos la URL de la imagen

Proveedor elegido: MySQL en Aiven

📐 Modelo Entidad-Relación 🗄️ Base de datos

El sistema se diseñó simple pero funcional.

🧑‍🍳 Tabla: usuarios

| Campo    | Tipo                    | Descripción   |
| -------- | ----------------------- | ------------- |
| id       | PK                      | Identificador |
| nombre   | VARCHAR                 | Nombre        |
| apellido | VARCHAR                 | Apellido      |
| email    | VARCHAR UNIQUE          | Login         |
| password | VARCHAR                 | Hash Argon2   |
| telefono | VARCHAR                 | Teléfono      |
| edad     | INT                     | Edad          |
| alergias | TEXT                    | Alergias      |
| rol      | ENUM('admin','cliente') | Permisos      |
| DNI      | varchar                 | Permisos      |

📌 Existe un admin por defecto:
admin@restaurante.com
/ admin123 (hasheado)

🍽 🍽 Tabla menus (menú por fecha) ( las fotos guardamos url de un book en cloudynary)

| Campo       | Tipo        | Descripción     |
| ----------- | ----------- | --------------- |
| id          | PK          | Identificador   |
| fecha       | DATE UNIQUE | Un menú por día |
| nombre      | VARCHAR     | Nombre menú     |
| descripcion | TEXT        | Detalles        |
| foto_url    | VARCHAR     | Imagen          |
| precio      | DECIMAL     | Precio          |

🧩 Tabla platos (Carta del restaurante)

| Campo            | Tipo    |
| ---------------- | ------- |
| id               | PK      |
| categoria        | VARCHAR |
| nombre           | VARCHAR |
| descripcion      | TEXT    |
| precio           | DECIMAL |
| ingredientes     | TEXT    |
| alergenos        | TEXT    |
| info_nutricional | TEXT    |
| imagen_url       | VARCHAR |
| activo           | BOOLEAN |

🪑 Tabla: mesas

| Campo       | Tipo       |
| ----------- | ---------- |
| id          | PK         |
| numero_mesa | INT UNIQUE |
| capacidad   | INT        |

📅 Tabla reservas

| Campo      | Tipo          |
| ---------- | ------------- |
| id         | PK            |
| usuario_id | FK → usuarios |
| mesa_id    | FK → mesas    |
| fecha      | DATE          |
| hora       | TIME          |
| party_size | INT           |
| estado     | ENUM          |
| resena     | TEXT          |

📌 Validación: una mesa no puede reservarse dos veces el mismo día.

🛍 Tabla: pedidos ( hecha por si hacemos la seccion de pedidos a domicilio)

| Campo             | Tipo                                                                   |
| ----------------- | ---------------------------------------------------------------------- |
| id                | INT (PK, AI)                                                           |
| usuario_id        | INT (FK → usuarios.id)                                                 |
| menu_id           | INT (FK → menus.id)                                                    |
| direccion_entrega | TEXT                                                                   |
| telefono_contacto | VARCHAR(20)                                                            |
| fecha_pedido      | DATETIME                                                               |
| estado            | ENUM('pendiente','en_preparacion','en_camino','entregado','cancelado') |
| cantidad          | INT                                                                    |
| total             | DECIMAL(10,2)                                                          |

4️⃣ Reglas de Negocio:

🔓 Menús públicos: se pueden consultar sin login
🔐 Reservas requieren login
🚫 Antes de reservar una mesa se debe validar que no esté ocupada en esa fecha
👑 Rol admin gestiona menús y mesas
👤 Rol cliente puede reservar y cancelar

5️⃣ 🔌 Conexión Backend ↔ Base de Datos

Creamos .env con credenciales Aiven:

MYSQL_HOST=xxxxx.aivencloud.com
MYSQL_PORT=11862
MYSQL_USER=avnadmin
MYSQL_PASSWORD=xxxxxx
MYSQL_DATABASE=defaultdb
MYSQL_CA_CERT=db/aiven-ca.pem

config.py

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

6️⃣ 🧪 Test de conexión

Creamos routes/test_db_routes.py

from fastapi import APIRouter
from config import get_conexion

router = APIRouter()

@router.get("/test-db")
async def test_db():
conn = await get_conexion()
async with conn.cursor() as cursor:
await cursor.execute("SELECT 1")
result = await cursor.fetchone()
conn.close()
return {"db_response": result}

En main.py:

app.include_router(test_db_routes.router, prefix="/debug", tags=["debug"])

Probar en:
http://127.0.0.1:8000/debug/test-db

✔ Si devuelve { "db_response": (1,) } la conexión funciona

#########################################################################

🚀 SIGUIENTE PASO —

📡 Rutas del Backend

🔐 AUTH (registro y login)

➕ POST /auth/register

Qué hace: crea un usuario (por defecto rol="cliente").
Validación interna: antes de insertar, el backend hace SELECT ... WHERE email = ? para asegurar que no exista.

Body:

POST {{host}}:{{port}}/auth/register
Content-Type: application/json

{
"nombre": "Laura",
"apellido": "Montironi",
"email": "laura@demo.com",
"telefono": "+34 600 000 000",
"edad": 25,
"alergias": "Sésamo",
"password": "Demo1234"
}

Response:==> FRONTED TYPE<{register_response: RegisterResponse}>

TYPE : RegisterResponse = {
msg: string;
item: IUsuario;
};

HTTP/1.1 201 Created
date: Sun, 08 Feb 2026 06:24:14 GMT
server: uvicorn
content-length: 199
content-type: application/json
connection: close

{
"msg": "usuario registrado correctamente",
"item": {
"id": 5,
"nombre": "Laura",
"apellido": "Montironi",
"email": "laura@demo.com",
"telefono": "+34 600 000 000",
"edad": 25,
"alergias": "Sésamo",
"rol": "cliente"

}

🔑 POST /auth/login

Descripción: Login usuario

Body:

{
"email": "laura@demo.com",
"password": "Demo1234"
}

Response: ==> FRONTED type LoginResponse = {
message: string;
token: string;
user:IUsuario;
};

HTTP/1.1 200 OK
date: Sun, 08 Feb 2026 06:25:19 GMT
server: uvicorn
content-length: 384
content-type: application/json
connection: close

{
"msg": "Login correcto",
"Token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NSwiZW1haWwiOiJsYXVyYUBkZW1vLmNvbSIsIm5vbWJyZSI6IkxhdXJhIiwicm9sIjoiY2xpZW50ZSIsImV4cCI6MTc3MDUzNTUyMX0.Er1xCu9HD8-R25OTYw_w0C3b7J8XqBSzSkhcWiEbVF4",
"user": {
"id": 5,
"nombre": "Laura",
"apellido": "Montironi",
"email": "laura@demo.com",
"telefono": "+34 600 000 000",
"edad": 25,
"alergias": "Sésamo",
"rol": "cliente"
}
}

❌ Response (credenciales incorrectas):

HTTP/1.1 500 Internal Server Error
date: Fri, 06 Feb 2026 14:03:49 GMT
server: uvicorn
content-length: 48
content-type: application/json
connection: close

{
"detail": "Error: 401: Credenciales inválidas"
}

👤 USUARIOS (requiere token)

🔍 GET /usuarios/{id} (token requerido)

Admin puede ver cualquiera / Cliente solo su propio id

Devuelve datos del usuario logueado

🍽 MENÚS (públicos por fecha )

| Método | Ruta             |              |
| ------ | ---------------- | ------------ |
| GET    | `/menus`         | Lista menús  |
| GET    | `/menus/{fecha}` | Menú por día |

Frontend type:
type IMenu = {
id:number;
fecha:string;
nombre:string;
descripcion:string;
foto_url:string;
precio:number;
}

Admin

| Método | Ruta          |
| ------ | ------------- |
| POST   | `/menus`      |
| PUT    | `/menus/{id}` |
| DELETE | `/menus/{id}` |

🍣 PLATOS ( carta digital)

| Método | Ruta                               |
| ------ | ---------------------------------- |
| GET    | `/platos/platos`                   |
| GET    | `/platos/platos/{id}`              |
| GET    | `/platos/platos?categoria=sashimi` |
| POST   | `/platos` (admin)                  |
| PUT    | `/platos/{id}` (admin)             |
| DELETE | `/platos/{id}` (admin)             |

🪑 MESAS

| Método | Ruta          | Acceso  |
| ------ | ------------- | ------- |
| GET    | `/mesas`      | Público |
| POST   | `/mesas`      | Admin   |
| PUT    | `/mesas/{id}` | Admin   |
| DELETE | `/mesas/{id}` | Admin   |

📅 RESERVAS

cliente
| Método | Ruta |
| ------ | ------------------------- |
| POST | `/reservas` |
| GET | `/reservas/me` |
| PUT | `/reservas/{id}/cancelar` |
| PUT | `/reservas/{id}/resena` |

Admin

| Método | Ruta                          |
| ------ | ----------------------------- |
| GET    | `/reservas`                   |
| GET    | `/reservas?with_reviews=true` |

🧩 Cómo funciona el sistema para el usuario

Cliente entra → ve carta o menús
Si quiere reservar → login
Reserva → asociada a su cuenta
Después puede dejar reseña

Admin entra → gestiona carta, menús y mesas → revisa actividad

🧪 Estado actual del backend

✅ Entorno configurado
✅ MySQL Aiven conectado
✅ JWT Auth funcionando
✅ Carta (platos)
✅ Menús por fecha
✅ Mesas
✅ Reservas

Rutas para e frontend indispensables :

✅ POST /auth/register
✅ POST /auth/login
✅ GET /menus (listar) => boton ver menú
✅ GET /menus/{fecha} (por fecha)
✅ POST /menus (admin)
✅ PUT /menus/{id} (admin)
✅ DELETE /menus/{id} (admin)
✅ GET /platos/platos (carta) => boton ver platos
✅ GET /platos/platos/{id} (ficha)
