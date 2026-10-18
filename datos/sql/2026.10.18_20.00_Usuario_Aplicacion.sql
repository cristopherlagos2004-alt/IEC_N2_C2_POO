-- Usuario de la aplicación con privilegios mínimos (ejecutar como root).
-- Solo puede leer y modificar datos; no puede borrar tablas ni crear usuarios.
-- Cambie 'cambiar_esta_contraseña' por una contraseña propia y úsela en el .env
CREATE USER IF NOT EXISTS 'usuario_escolar'@'localhost'
    IDENTIFIED WITH caching_sha2_password BY 'cambiar_esta_contraseña';
GRANT SELECT, INSERT, UPDATE, DELETE ON gestion_escolar.* TO 'usuario_escolar'@'localhost';
FLUSH PRIVILEGES;
