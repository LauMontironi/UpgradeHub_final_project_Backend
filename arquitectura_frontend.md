# Arquitectura Frontend (UpgradeFood) — Qué pantallas hay y de dónde salen los datos

## 1) Landing Page (Home)

**Objetivo:** que el usuario entre y entienda rápido qué puede hacer.

### ✅ Componentes

- **Navbar (componente)** con links que cambian según si estás logueado o no (con `@if` como lo hizo Mario):
  - Si NO estás logueado: `Logo | Register | Login`
  - Si estás logueado: `Logo | Reservas | Pedidos (si lo usamos) | Logout`
  - (y también “Ver Menú” / “Ver Platos” accesible para todos)

### ✅ Secciones Landing

- **Hero central** (foto grande con el efecto “pasarela” del Yami Food)
  - Texto/frase en el centro
  - 2 botones:
    - **Ver Menú**
    - **Ver Nuestros Platos**
- Más abajo:
  - **Mapa / ubicación** (igual que Yami Food)
- **Footer (componente)** con links + info + alguna sección tipo artículos como el Yami Food

📌 _Esta página no necesita login para ver menú/platos._

---

## 2) Página “Menús” (lo que pide el PDF)

**Esta es la pantalla clave del enunciado:** el usuario ve **5/7 menús** (o los 7) y elige uno.

### ✅ Qué ve el usuario

- Cards tipo:
  - **Menú 1** (título)
  - precio
  - descripción corta
  - (opcional: alérgenos generales si queremos ponerlos)
- Cuando el usuario clica:
  - botón **“Ver especificaciones”** → abre el detalle del menú con los 3 platos
  - y si está logueado, aparece botón **“Reservar”**

### 🗄️ Tablas implicadas

- `menus_semanales` → lista de menús 1–7 (título, descripción, precio)
- `menu_semanal_platos` → relación menú ↔ platos con el rol (entrante/principal/postre)
- `platos` → para traer la ficha completa de cada plato (foto, ingredientes, alérgenos, info nutricional)

### 🔥 Rutas backend que usa esta página

- Listar todos los menús:
  - **GET** `{{host}}:{{port}}/menus-semanales`
  - devuelve los 7 menús (id, numero, título, descripción, precio)
- Ver un menú completo (con sus 3 platos + sus fotos + su info):
  - **GET** `{{host}}:{{port}}/menus-semanales/1`
  - (y lo mismo para 2…7)

### 🧩 Qué hace Angular

- En `ngOnInit()`:
  - llamar al service: `getMenusSemanales()`
  - pintar cards con el array
- Al clicar en un menú:
  - navegar a `/menus/:id`
  - en esa página llamar `getMenuSemanalDetalle(id)`
  - renderizar:
    - el menú
    - los 3 platos en cards (con imagen y todo)

---

## 3) Página “Detalle Menú” (cuando clicas un menú)

**Objetivo:** ver el menú por dentro: entrante + principal + postre, cada uno con su ficha.

### ✅ Qué se ve

- Cabecera del menú (título, precio, descripción)
- 3 cards (o una sección por rol):
  - Entrante
  - Principal
  - Postre
    Cada plato muestra:
- imagen
- nombre
- descripción
- ingredientes
- alérgenos
- info nutricional

### 🗄️ Tabla principal

- `platos` (porque ahí está toda la info real)
- (la relación la hace `menu_semanal_platos`)

### 🔥 Ruta backend

- **GET** `{{host}}:{{port}}/menus-semanales/:id`

### ✅ Botones en esta pantalla

- “Reservar este menú” (solo si el usuario está logueado)

---

## 4) Página “Nuestros Platos” (carta completa)

**Objetivo:** mostrar todos los platos individuales con carrusel o grid por categorías.

### ✅ Qué se ve

- Carrusel / grid con platos
- filtros por categoría (entrantes, sashimi, nigiri, maki, bao, postre)
- al clicar un plato → ficha completa (modal o ruta /platos/:id)

### 🗄️ Tabla

- `platos`

### 🔥 Ruta backend

- **GET** `{{host}}:{{port}}/platos/platos`

---

## 5) Registro

**Objetivo:** crear usuario con los campos que pide la tabla.

### 🗄️ Tabla

- `usuarios`

### Datos que pide el registro

- nombre
- apellido
- email
- teléfono
- edad
- password
- (alergias opcional)

### 🔥 Ruta backend

- **POST** `{{host}}:{{port}}/auth/register`

Después de registrar:

- te redirige al login

---

## 6) Login

**Objetivo:** iniciar sesión y guardar token.

### 🔥 Ruta backend

- **POST** `{{host}}:{{port}}/auth/login`

UX :

- puede ser una página o un popup/modal
- cuando loguea bien: alert / pantalla “login correcto” como dijo Mario

---

## 7) Reservas (flujo real del usuario)

Esto es lo que entendemos como experiencia:

- Cliente entra → **Ver menús**
- Ve **Menú 1–7** (packs)
- Clica Menú 1 → ve sus 3 platos (con imágenes y fichas)
- Pulsa **Reservar** → elige fecha/hora/personas
- Se crea la reserva y queda asociado qué menú eligió

📌 (Aquí falta confirmar en backend cómo guardaremos esa asociación: lo suyo sería añadir `menu_semanal_id` en `reservas`).

---

# Resumen rápido

### Páginas principales

1. `/` Landing
2. `/menus` lista menús 1–7
3. `/menus/:id` detalle menú con platos
4. `/platos` carta completa
5. `/register`
6. `/login`
7. `/reservas` (cuando esté)
   pedidos?¿ no se si no es complicarse de mas

### Rutas backend clave ahora

- `GET /menus-semanales` → lista packs 1–7
- `GET /menus-semanales/:id` → menú + 3 platos con toda su info
- `GET /platos/platos` → carta completa
- `POST /auth/register`
- `POST /auth/login`
