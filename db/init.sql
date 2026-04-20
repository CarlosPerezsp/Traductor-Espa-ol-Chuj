-- ALMG Translator - Initial Schema

CREATE TABLE IF NOT EXISTS languages (
    id   INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(10)  NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS categories (
    id   INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS translations (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    source_text  VARCHAR(500) NOT NULL,
    target_text  VARCHAR(500) NOT NULL,
    source_lang  INT NOT NULL,
    target_lang  INT NOT NULL,
    category_id  INT,
    notes        TEXT,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (source_lang) REFERENCES languages(id),
    FOREIGN KEY (target_lang) REFERENCES languages(id),
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- Seed: languages
INSERT INTO languages (code, name) VALUES
    ('es',   'Español'),
    ('chuj', 'Chuj');

-- Seed: categories
INSERT INTO categories (name) VALUES
    ('Saludos'),
    ('Números'),
    ('Animales'),
    ('Colores'),
    ('Familia'),
    ('General');

-- Seed: sample translations (Español → Chuj)
INSERT INTO translations (source_text, target_text, source_lang, target_lang, category_id) VALUES
    ('Hola',         'Kolawal',    1, 2, 1),
    ('Buenos días',  'Wach" k"u', 1, 2, 1),
    ('Gracias',      'YujwalYos',    1, 2, 6),
    ('Uno',          'Juun',        1, 2, 2),
    ('Dos',          'Chab',       1, 2, 2),
    ('Tres',         'Oxe',       1, 2, 2);
