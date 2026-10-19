-- Usuario de la aplicación con privilegios mínimos (ejecutar como root).
-- Solo puede leer y modificar datos; no puede borrar tablas ni crear usuarios.
-- NO edite este archivo (la contraseña terminaría en GitHub): copie estos comandos
-- en MySQL, cambie 'cambiar_esta_contraseña' por una propia y úsela en su .env
CREATE USER IF NOT EXISTS 'usuario_escolar'@'localhost'
    IDENTIFIED WITH caching_sha2_password BY 'cambiar_esta_contraseña';
GRANT SELECT, INSERT, UPDATE, DELETE ON gestion_escolar.* TO 'usuario_escolar'@'localhost';
FLUSH PRIVILEGES;
