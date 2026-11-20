-- Evaluación 3: tabla de usuarios para el inicio de sesión.
-- La contraseña NUNCA se guarda: solo su hash bcrypt (60 caracteres, incluye la sal).
-- Los usuarios se crean con el script crear_usuario.py (no con INSERT a mano),
-- porque el hash lo calcula Python.
USE gestion_escolar;

CREATE TABLE IF NOT EXISTS usuarios(
    id_usuario INTEGER AUTO_INCREMENT,
    nombre_usuario VARCHAR(30) NOT NULL,
    hash_contrasena VARCHAR(255) NOT NULL,
    intentos_fallidos INTEGER NOT NULL DEFAULT 0,
    bloqueado_hasta DATETIME NULL,
    CONSTRAINT pk_usuarios PRIMARY KEY (id_usuario),
    CONSTRAINT uq_usuarios_nombre UNIQUE (nombre_usuario),
    CONSTRAINT ck_usuarios_intentos CHECK (intentos_fallidos >= 0)
) COMMENT = 'Usuarios que pueden iniciar sesion en el sistema';
