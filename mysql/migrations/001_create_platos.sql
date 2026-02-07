CREATE TABLE platos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    categoria ENUM(
        'entrante',
        'sashimi',
        'nigiri',
        'maki',
        'bao',
        'postre'
    ) NOT NULL,
    nombre VARCHAR(160) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10, 2) NOT NULL,
    ingredientes TEXT,
    alergenos TEXT,
    info_nutricional TEXT,
    imagen_url VARCHAR(500),
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO
    platos (
        categoria,
        nombre,
        descripcion,
        precio,
        ingredientes,
        alergenos,
        info_nutricional,
        imagen_url,
        activo
    )
VALUES

-- 🥢 ENTRANTES
(
    'entrante',
    'Edamame al vapor',
    'Vainas de soja tiernas al vapor con sal marina.',
    4.50,
    'Soja verde, sal marina.',
    'Soja.',
    'Bajo en calorías, alto en proteína vegetal y fibra.',
    'https://res.cloudinary.com/dej3mecyv/image/upload/v1770497579/Edamame_al_vapor_thqxap.jpg',
    TRUE
),
(
    'entrante',
    'Gyozas de cerdo',
    'Empanadillas japonesas rellenas de cerdo y verduras.',
    6.90,
    'Cerdo, col china, cebollino, ajo, jengibre, masa de trigo.',
    'Gluten, soja.',
    'Ricas en proteína, moderadas en grasa.',
    'https://res.cloudinary.com/dej3mecyv/image/upload/v1770497579/Gyozas_de_cerdo_jhr8r2.jpg',
    TRUE
),
(
    'entrante',
    'Tempura de verduras',
    'Verduras de temporada en tempura ligera y crujiente.',
    7.50,
    'Calabacín, zanahoria, berenjena, harina tempura.',
    'Gluten.',
    'Fritura ligera, consumo moderado recomendado.',
    'https://res.cloudinary.com/dej3mecyv/image/upload/v1770497589/Tempura_de_verduras_cjfogc.jpg',
    TRUE
),
(
    'entrante',
    'Wakame salad',
    'Ensalada de algas wakame aliñada con sésamo.',
    5.50,
    'Alga wakame, sésamo, vinagre de arroz.',
    'Sésamo.',
    'Baja en calorías, rica en minerales.',
    'https://res.cloudinary.com/dej3mecyv/image/upload/v1770497591/Wakame_salad_zqrapd.jpg',
    TRUE
),
(
    'entrante',
    'Karaage de pollo',
    'Pollo marinado al estilo japonés, frito y crujiente.',
    7.90,
    'Pollo, soja, jengibre, ajo, fécula de patata.',
    'Soja.',
    'Alto en proteína, frito.',
    'https://res.cloudinary.com/dej3mecyv/image/upload/v1770497580/Karaage_de_pollo_wrf2dc.jpg',
    TRUE
),

-- 🍣 SASHIMI
(
    'sashimi',
    'Sashimi de salmón',
    'Salmón fresco cortado en láminas gruesas.',
    12.90,
    'Salmón.',
    'Pescado.',
    'Alto en omega-3 y proteína.',
    'https://res.cloudinary.com/dej3mecyv/image/upload/v1770497586/Sashimi_de_salm%C3%B3n_brpqdg.jpg',
    TRUE
),
(
    'sashimi',
    'Sashimi de atún rojo',
    'Atún rojo de calidad premium.',
    15.90,
    'Atún rojo.',
    'Pescado.',
    'Rico en proteína y hierro.',
    'https://res.cloudinary.com/dej3mecyv/image/upload/v1770497585/Sashimi_de_at%C3%BAn_rojo_h9rudt.jpg',
    TRUE
),
(
    'sashimi',
    'Sashimi de lubina',
    'Lubina fresca de sabor delicado.',
    13.50,
    'Lubina.',
    'Pescado.',
    'Bajo en grasa, alto en proteína.',
    'https://res.cloudinary.com/dej3mecyv/image/upload/v1770497586/Sashimi_de_lubina_q2cjue.jpg',
    TRUE
),
(
    'sashimi',
    'Sashimi mixto',
    'Selección del día de pescados frescos.',
    16.90,
    'Salmón, atún, pescado blanco.',
    'Pescado.',
    'Combinación rica en proteínas y omega-3.',
    'https://res.cloudinary.com/dej3mecyv/image/upload/v1770497588/Sashimi_mixto_t0sjch.jpg',
    TRUE
),
(
    'sashimi',
    'Sashimi de vieira',
    'Vieira fresca, suave y ligeramente dulce.',
    14.90,
    'Vieira.',
    'Moluscos.',
    'Bajo en grasa, alto en minerales.',
    'https://res.cloudinary.com/dej3mecyv/image/upload/v1770497588/Sashimi_de_vieira_qyakhc.jpg',
    TRUE
),

-- 🍙 NIGIRI
(
    'nigiri',
    'Nigiri de salmón',
    'Arroz avinagrado con salmón fresco.',
    4.50,
    'Arroz sushi, salmón.',
    'Pescado.',
    'Equilibrio entre carbohidratos y proteína.',
    'https://res.cloudinary.com/dej3mecyv/image/upload/v1770497583/Nigiri_de_salm%C3%B3n_imf1xw.jpg',
    TRUE
),
(
    'nigiri',
    'Nigiri de atún',
    'Clásico nigiri de atún rojo.',
    5.50,
    'Arroz sushi, atún.',
    'Pescado.',
    'Rico en proteína magra.',
    'https://res.cloudinary.com/dej3mecyv/image/upload/v1770497583/Nigiri_de_at%C3%BAn_id5djy.jpg',
    TRUE
),
(
    'nigiri',
    'Nigiri de langostino',
    'Langostino cocido sobre arroz sushi.',
    4.90,
    'Arroz sushi, langostino.',
    'Crustáceos.',
    'Bajo en grasa, alto en proteína.',
    'https://res.cloudinary.com/dej3mecyv/image/upload/v1770497583/Nigiri_de_langostino_wm0f7a.jpg',
    TRUE
),
(
    'nigiri',
    'Nigiri de anguila',
    'Anguila glaseada con salsa kabayaki.',
    6.50,
    'Arroz sushi, anguila, salsa kabayaki.',
    'Pescado, soja.',
    'Más calórico por la salsa.',
    'https://res.cloudinary.com/dej3mecyv/image/upload/v1770497582/Nigiri_de_anguila_mceouq.jpg',
    TRUE
),
(
    'nigiri',
    'Nigiri de tamago',
    'Tortilla japonesa dulce sobre arroz.',
    4.00,
    'Huevo, azúcar, arroz sushi.',
    'Huevo.',
    'Fuente de proteína y carbohidratos.',
    'https://res.cloudinary.com/dej3mecyv/image/upload/v1770497585/Nigiri_de_tamago_gyez2u.jpg',
    TRUE
),

-- 🍣 MAKIS
(
    'maki',
    'California roll',
    'Rollo de arroz con cangrejo, aguacate y pepino.',
    8.90,
    'Arroz sushi, cangrejo, aguacate, pepino, nori.',
    'Crustáceos.',
    'Equilibrado, contiene grasas saludables.',
    'https://res.cloudinary.com/dej3mecyv/image/upload/v1770497579/California_roll_s4abez.jpg',
    TRUE
),
(
    'maki',
    'Maki de salmón',
    'Maki clásico de salmón fresco.',
    8.50,
    'Arroz sushi, salmón, alga nori.',
    'Pescado.',
    'Rico en omega-3.',
    'https://res.cloudinary.com/dej3mecyv/image/upload/v1770497581/Maki_de_salm%C3%B3n_imf1xw.jpg',
    TRUE
),
(
    'maki',
    'Spicy tuna roll',
    'Atún con salsa picante japonesa.',
    9.50,
    'Atún, mayonesa picante, arroz, nori.',
    'Pescado, huevo.',
    'Moderado en grasas por la salsa.',
    'https://res.cloudinary.com/dej3mecyv/image/upload/v1770497589/Spicy_tuna_roll_uwbetm.jpg',
    TRUE
),
(
    'maki',
    'Tempura shrimp roll',
    'Langostino en tempura con salsa dulce.',
    10.90,
    'Langostino, harina tempura, arroz, nori.',
    'Gluten, crustáceos.',
    'Fritura ligera.',
    'https://res.cloudinary.com/dej3mecyv/image/upload/v1770497589/Tempura_shrimp_roll_k4bciq.jpg',
    TRUE
),
(
    'maki',
    'Maki vegetal',
    'Rollo vegetariano con verduras frescas.',
    7.90,
    'Aguacate, pepino, zanahoria, arroz, nori.',
    'Ninguno.',
    'Bajo en grasas, apto vegetariano.',
    'https://res.cloudinary.com/dej3mecyv/image/upload/v1770497582/Maki_vegetal_ziby4n.jpg',
    TRUE
),

-- 🥪 BAO
(
    'bao',
    'Bao de cerdo teriyaki',
    'Pan bao al vapor relleno de cerdo glaseado.',
    5.90,
    'Pan bao, cerdo, salsa teriyaki.',
    'Gluten, soja.',
    'Alto en carbohidratos y proteína.',
    'https://res.cloudinary.com/dej3mecyv/image/upload/v1770497579/Bao_de_cerdo_teriyaki_sjedge.jpg',
    TRUE
),
(
    'bao',
    'Bao de pollo crujiente',
    'Pollo frito con mayonesa japonesa.',
    5.90,
    'Pan bao, pollo, mayonesa japonesa.',
    'Gluten, huevo.',
    'Moderado en grasas.',
    'https://res.cloudinary.com/dej3mecyv/image/upload/v1770497579/Bao_de_pollo_crujiente_sdbqtb.jpg',
    TRUE
),
(
    'bao',
    'Bao de salmón',
    'Salmón marinado con salsa ponzu.',
    6.50,
    'Pan bao, salmón, ponzu.',
    'Gluten, pescado, soja.',
    'Rico en proteínas.',
    'https://res.cloudinary.com/dej3mecyv/image/upload/v1770497579/Bao_de_salm%C3%B3n_xhlpl8.jpg',
    TRUE
),
(
    'bao',
    'Bao vegetal',
    'Verduras salteadas con salsa de soja.',
    5.50,
    'Pan bao, verduras, soja.',
    'Gluten, soja.',
    'Opción vegetal ligera.',
    'https://res.cloudinary.com/dej3mecyv/image/upload/v1770497579/Bao_vegetal_e72kcf.jpg',
    TRUE
),
(
    'bao',
    'Bao de langostino',
    'Langostino en tempura con salsa picante.',
    6.90,
    'Pan bao, langostino, tempura.',
    'Gluten, crustáceos.',
    'Fritura ligera.',
    'https://res.cloudinary.com/dej3mecyv/image/upload/v1770497579/Bao_de_langostino_xwb2in.jpg',
    TRUE
),

-- 🍡 POSTRES
(
    'postre',
    'Mochi de matcha',
    'Mochi japonés relleno de crema de té matcha.',
    4.90,
    'Harina de arroz, azúcar, té matcha, nata.',
    'Lácteos.',
    'Alto en carbohidratos.',
    'https://res.cloudinary.com/dej3mecyv/image/upload/v1770497582/Mochi_de_matcha_kijzgr.jpg',
    TRUE
),
(
    'postre',
    'Mochi de chocolate',
    'Mochi suave relleno de crema de chocolate.',
    4.90,
    'Harina de arroz, cacao, azúcar, nata.',
    'Lácteos.',
    'Alto en carbohidratos.',
    'https://res.cloudinary.com/dej3mecyv/image/upload/v1770497582/Mochi_de_chocolate_p80x9z.jpg',
    TRUE
),
(
    'postre',
    'Dorayaki',
    'Bizcocho japonés relleno de judía roja dulce.',
    5.50,
    'Harina de trigo, huevo, azúcar, judía roja.',
    'Gluten, huevo.',
    'Energético, alto en carbohidratos.',
    'https://res.cloudinary.com/dej3mecyv/image/upload/v1770497579/Dorayaki_txjqg2.jpg',
    TRUE
),
(
    'postre',
    'Cheesecake de yuzu',
    'Tarta de queso cremosa con toque cítrico de yuzu.',
    6.50,
    'Queso crema, huevo, azúcar, yuzu, galleta.',
    'Lácteos, gluten, huevo.',
    'Alto en grasas y azúcares.',
    'https://res.cloudinary.com/dej3mecyv/image/upload/v1770497579/Cheesecake_de_yuzu_agcr6f.jpg',
    TRUE
),
(
    'postre',
    'Helado de sésamo negro',
    'Helado artesanal de sésamo negro.',
    4.50,
    'Leche, nata, azúcar, sésamo negro.',
    'Lácteos, sésamo.',
    'Alto en grasas.',
    'https://res.cloudinary.com/dej3mecyv/image/upload/v1770497580/Helado_de_s%C3%A9samo_negro_nvoxaj.jpg',
    TRUE
);

UPDATE platos
SET
    imagen_url = 'https://res.cloudinary.com/dej3mecyv/image/upload/v1770497584/Nigiri_de_salm%C3%B3n_ygbheh.jpg'
WHERE
    nombre = 'Nigiri de salmón';