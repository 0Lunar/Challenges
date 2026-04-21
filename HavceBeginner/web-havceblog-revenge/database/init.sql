CREATE DATABASE IF NOT EXISTS havceblog;

USE havceblog;

CREATE USER IF NOT EXISTS 'utente_db'@'%' IDENTIFIED BY 'Ciao1234oaiC';

GRANT
    CREATE,
    INSERT,
    SELECT,
    UPDATE
ON havceblog.*
TO 'utente_db'@'%';

FLUSH PRIVILEGES;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    displayname VARCHAR(32) NOT NULL,
    username VARCHAR(32) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    lastlogin TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    role ENUM('admin', 'writer', 'user') NOT NULL
);

CREATE TABLE IF NOT EXISTS posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title TEXT NOT NULL,
    content LONGTEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    id_author INT DEFAULT NULL,
    FOREIGN KEY (id_author) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS secrets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title TEXT NOT NULL,
    content LONGTEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

INSERT INTO users (displayname, username, password, role) VALUES
('Admin', 'admin', '$2a$12$hashed_password_1_simulated', 'admin'),
('Writer1', 'writer1', '$2a$12$hashed_password_2_simulated', 'writer'),
('User1', 'user1', '$2a$12$hashed_password_3_simulated', 'user');

INSERT INTO posts (title, content, id_author) VALUES
('Primo Post', 'Questo è il contenuto del primo post.', 1),
('Secondo Post', '## Contenuto interessante scritto da Writer1.\ntest *test* **test**', 2),
('Terzo Post', 'Un altro contenuto di esempio.', 3);

INSERT INTO secrets (title, content) VALUES
('Ricetta carbonara', 'Panna, Bacon, Rigatoni, Cipolla, Rucola, Mela a fette'),
('Ricetta flag', 'Voglia di lavorare, impegno, conoscenze, havceCTF{REDACTED}'),
('Ricetta pizza', 'Acqua, Panna, Latte, Formaggio in polvere');
