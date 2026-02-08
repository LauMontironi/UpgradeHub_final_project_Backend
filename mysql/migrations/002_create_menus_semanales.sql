-- =========================
-- MENÚS SEMANALES (1 al 7)
-- =========================
CREATE TABLE menus_semanales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero TINYINT NOT NULL UNIQUE, -- 1..7
    titulo VARCHAR(160) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10, 2) NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================================
-- RELACIÓN: qué platos tiene cada menú (3)
-- =========================================
CREATE TABLE menu_semanal_platos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    menu_id INT NOT NULL,
    plato_id INT NOT NULL,
    rol ENUM(
        'entrante',
        'principal',
        'postre'
    ) NOT NULL,
    UNIQUE KEY uq_menu_rol (menu_id, rol), -- evita 2 entrantes en el mismo menú
    FOREIGN KEY (menu_id) REFERENCES menus_semanales (id) ON DELETE CASCADE,
    FOREIGN KEY (plato_id) REFERENCES platos (id) ON DELETE RESTRICT
);

INSERT INTO menu_semanal_platos (menu_id, plato_id, rol) VALUES

-- MENÚ 1
(1, 3, 'entrante'), (1, 13, 'principal'), (1, 28, 'postre'),

-- MENÚ 2
(2, 4, 'entrante'), (2, 19, 'principal'), (2, 29, 'postre'),

-- MENÚ 3
(3, 5, 'entrante'), (3, 18, 'principal'), (3, 30, 'postre'),

-- MENÚ 4
(4, 6, 'entrante'), (4, 20, 'principal'), (4, 31, 'postre'),

-- MENÚ 5
(5, 7, 'entrante'), (5, 21, 'principal'), (5, 32, 'postre'),

-- MENÚ 6
(6, 3, 'entrante'), (6, 23, 'principal'), (6, 28, 'postre'),

-- MENÚ 7
(7, 4, 'entrante'), (7, 24, 'principal'), (7, 29, 'postre');