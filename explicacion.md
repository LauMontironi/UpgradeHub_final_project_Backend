Cómo funciona el backend de UpgradeFood (explicado)

Este backend representa la operativa básica de un restaurante: clientes que consultan menús y reservan, y un administrador (dueño) que gestiona menús, mesas y puede revisar reseñas y actividad.

La aplicación maneja dos tipos de usuarios:

1. Cliente (rol = cliente)

Puede ver los menús sin estar logueado.

Pero si quiere reservar una mesa o hacer un pedido, necesita estar autenticado (logueado) porque el sistema debe saber quién es y guardar sus acciones asociadas a su cuenta.

Puede ver sus propias reservas, cancelarlas y escribir una reseña después de disfrutar la reserva.

2. Administrador (rol = admin)

Es el “dueño del restaurante” dentro del sistema.

Puede crear, editar y borrar menús.

Puede definir mesas (cuántas hay y la capacidad de cada una).

Puede ver reseñas dejadas por clientes y revisar la actividad general.

Autenticación: cómo se controla el acceso

El registro y login generan un token (JWT).

Ese token se envía en cada request privado con:

Authorization: Bearer <token>

Con ese token el backend sabe:

qué usuario hace la petición

su id

su rol (admin o cliente)

Con eso se aplican permisos:

admin: puede hacer POST/PUT/DELETE de recursos clave.

cliente: puede crear reservas/pedidos y ver solo lo suyo.

Tablas de la base de datos y para qué sirven
🧑‍🍳 usuarios

Guarda las cuentas de la app (clientes y admin).

Campos clave:

id: identificador

nombre, email, password: credenciales

rol: define permisos (admin o cliente)

📌 Importante: existe un admin creado por defecto en la base con un INSERT inicial.Admin Principal admin@restaurante.com ckave admin123

🍽 menus

Guarda el menú de cada día.

Idea del sistema:

Hay un menú distinto por día, por eso fecha es única.

Las fotos NO se guardan en el frontend, se guarda solo foto_url (link), para poder cambiar imágenes/precios sin tocar Angular.

Campos:

fecha: día del menú (único)

nombre, descripcion, precio

foto_url: link público de imagen (unsplash podriamos tener un book en cloudflare)

🪑 mesas

Define las mesas físicas del restaurante.

Campos:

numero_mesa (único)

capacidad (2, 4, 6, etc.)

Esto lo gestiona el admin porque es parte del “inventario” del restaurante.

📅 reservas

Relaciona un cliente con una mesa y una fecha.

Campos clave:

usuario_id: quién reservó

mesa_id: qué mesa

fecha_reserva: para qué día

estado: confirmada o cancelada

resena: texto opcional que se completa después

📌 Regla importantísima:
Antes de crear una reserva, se valida disponibilidad: esa mesa no puede tener otra reserva activa en la misma fecha.

🛍 pedidos

Representa pedidos asociados a un usuario y un menú.

Campos clave:

usuario_id: quién compra

menu_id: qué menú compró

cantidad, total

direccion_entrega, telefono_contacto

estado: flujo del pedido (pendiente → en preparación → en camino → entregado / cancelado)

Rutas del backend y quién puede usarlas
✅ AUTH (públicas)

Estas rutas existen para crear cuenta y loguearse:

POST /auth/register

Crea un usuario (por defecto cliente)

Valida que el email no exista

POST /auth/login

Verifica credenciales

Devuelve token + datos del usuario

👤 USUARIOS (con token)

Estas rutas son para consultar datos de usuario.

GET /usuarios/{id}

Solo puede acceder:

el admin

o el propietario (si id es el suyo)

Sirve para cargar “mi perfil” o validar permisos.

🍽 MENÚS (públicas y admin)

Públicas (sin login):

GET /menu/ → lista todos los menús

GET /menu/{fecha} → menú por fecha (YYYY-MM-DD)

Admin (con token + rol admin):

POST /menu/ → crear menú del día

PUT /menu/{id} → editar un menú

DELETE /menu/{id} → borrar un menú

🪑 MESAS (admin y lectura para reservar)

GET /mesas/

Cliente puede verlas para elegir dónde reservar (o puede ser público si decidís)

POST /mesas/ (admin)

PUT /mesas/{id} (admin)

DELETE /mesas/{id} (admin)

📅 RESERVAS (cliente y admin)

Cliente autenticado:

POST /reservas/ → crear reserva (valida disponibilidad)

GET /reservas/me → ver mis reservas

PUT /reservas/{id}/cancelar → cancelar mi reserva

PUT /reservas/{id}/resena → escribir reseña (idealmente si ya pasó la fecha)

Admin:

GET /reservas/ → ver todas (incluidas reseñas)

🛍 PEDIDOS (cliente y admin si queréis)

Cliente autenticado:

POST /pedidos/ → crear pedido

GET /pedidos/me → ver mis pedidos

Admin (opcional pero típico):

GET /pedidos/ → ver todos

PUT /pedidos/{id}/estado → cambiar estado (pendiente → en preparación…)

Resumen final “en una frase”

Menús son públicos para consultar.

Para reservar y pedir, el cliente debe estar logueado.

El admin gestiona lo estructural del restaurante (mesas, menús) y revisa reseñas/actividad.

La base de datos conecta todo con relaciones: usuarios → reservas/pedidos, menús → pedidos, mesas → reservas.

🧩 Cómo funcionará tu sistema
1️⃣ Carta del restaurante (NUEVO)

El usuario puede entrar y ver todos los platos individuales:

Categorías:

Entrantes

Sashimi

Nigiris

Makis

Bao

Postres

Cada plato tendrá:

nombre

descripción

precio

ingredientes

alérgenos

información nutricional

imagen

GET /platos
GET /platos/{id}
GET /platos?categoria=sashimi
Esto es la carta digital del restaurante.

Menús del día
Ejemplo:

Menú 1 — Lunes

Entrante: Gyozas

Principal: Sushi variado

Postre: Mochi

Precio: 14,90 €

Descripción

Alérgenos

Info nutricional

Imagen (una de tus fotos)

| Función            | Tabla    | Quién la usa |
| ------------------ | -------- | ------------ |
| Ver carta completa | `platos` | Clientes     |
| Gestionar carta    | `platos` | Admin        |
| Ver menú del día   | `menus`  | Clientes     |
| Crear/editar menús | `menus`  | Admin        |
