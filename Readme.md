🍣 UpgradeFood — Documentación Backend Completa

Este backend representa la operativa de un restaurante real: clientes que consultan menús y reservan, y un administrador que gestiona menús, mesas, carta y revisa la actividad global del negocio.

🚀 Ver API en vivo (Swagger UI): https://upgradehubfinalproject-production.up.railway.app/docs#/

🛠️ Stack Tecnológico
Frontend: Angular 19+ (Signals, Standalone Components, Control Flow @if/@for).

Backend: FastAPI (Python 3.12) con programación asíncrona (aiomysql).

Base de Datos: MySQL gestionado en Aiven Cloud (Certificación SSL).

Seguridad: Autenticación JWT (JSON Web Tokens) y Hasheo Argon2.

Diseño: Bootstrap 5.3 + Custom CSS (Premium Dark & Gold Theme).

Cloud Hosting: Railway (Backend) y Cloudinary (Multimedia).

1️⃣ Configuración del Proyecto

# Creación del entorno de trabajo

mkdir ProyectoUpgrade
cd ProyectoUpgrade

# Entorno virtual y dependencias

python -m venv .venv
source .venv/Scripts/activate # Windows Git Bash

pip install "fastapi[standard]"
pip install aiomysql
pip install python-dotenv
pip install "passlib[argon2]"
pip install "python-jose[cryptography]"
pip freeze > requirements.txt

2️⃣ Infraestructura y Base de Datos (Aiven)

Decidimos que la base de datos no debía estar en localhost para asegurar la disponibilidad en producción y facilitar el trabajo colaborativo.

Proveedor: MySQL en Aiven Cloud.

Gestión de Imágenes: Las fotos NO se guardan en el servidor. Se almacenan en Cloudinary y en la base de datos solo guardamos la URL.

Seguridad: Conexión cifrada mediante certificado SSL (ca.pem).

📐 Modelo Entidad-Relación 🗄️ Base de datos

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

🍽 Tabla menus (menú por fecha) ( las fotos guardamos url de un book en cloudynary)

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

🔗 Tabla Puente: menu_semanal_platos (Relación N:M)
Esta tabla permite que un plato pertenezca a varios menús y que un menú tenga varios platos.

menu_id: FK → menus_semanales.id

plato_id: FK → platos.id

rol: ENUM ('entrante', 'principal', 'postre')

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

⭐ Tabla: resenas
| Campo | Tipo |
| ---------- | ----------------- - |
| id | PK ID de la reseña |
| usuario_id | FK → Cliente que comenta |
| comentario | TEXT Opinión escrita |
| puntuacion | INT Escala del 1 al 5 |

📡 Endpoints del Sistema (API REST)

🔐 Autenticación

POST /auth/register: Registro de nuevos clientes.

POST /auth/login: Genera un Token JWT para acceso protegido.

🍱 Gestión de Menús (Admin)

GET /menus: Lista todos los menús públicos.

POST /menus: Crea el contenedor del menú (Admin).

POST /menus-semanales/vincular-plato: Asigna platos específicos a un menú con un rol (Entrante/Principal/Postre).

DELETE /menus/{id}: Elimina un menú y sus vínculos.

🪑 Mesas y Reservas

GET /mesas: Listado de mesas y capacidades.

POST /reservas: El cliente reserva una mesa (Validación: no permite duplicados en fecha/hora).

GET /reservas/me: Historial de reservas del cliente logueado.

⭐ Reseñas

GET /resenas: Público. Muestra los comentarios en el Dashboard o Landing.

POST /resenas: Privado. Permite a los clientes valorar su experiencia.

4️⃣ Reglas de Negocio y Seguridad

Protección de Rutas (Guards): Las rutas de administración (/admin/\*\*) requieren que el usuario tenga un token válido y el rol admin.

Validación de Capacidad: No se permiten reservas si el número de personas excede la capacidad de la mesa seleccionada.

Integridad de Datos: Al eliminar un menú, se limpian automáticamente sus vínculos en la tabla puente para evitar datos huérfanos.

🔓 Menús públicos: se pueden consultar sin login
🔐 Reservas requieren login
🚫 Antes de reservar una mesa se debe validar que no esté ocupada en esa fecha
👑 Rol admin gestiona menús y mesas
👤 Rol cliente puede reservar y cancelar

🧪 Estado Actual del Proyecto
✅ Conexión Aiven SSL funcionando. ✅ Lógica de asignación de platos a menús terminada. ✅ Gestión de mesas con CRUD completo. ✅ Sistema de seguridad JWT implementado en Frontend y Backend.
