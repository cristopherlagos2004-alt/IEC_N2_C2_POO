-- Evaluación 3: tabla de usuarios del sistema (login).
-- La contraseña NO se guarda: se guarda su hash BCrypt (60 caracteres, empieza con $2b$).
-- Eliminación lógica: un usuario no se borra, se deshabilita con activo = 0.
USE gestion_escolar;

CREATE TABLE usuarios(
    id_usuario INTEGER AUTO_INCREMENT,
    nombre_usuario VARCHAR(30) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    clave_hash VARCHAR(255) NOT NULL,
    activo TINYINT(1) NOT NULL DEFAULT 1,
    ultimo_acceso DATETIME NULL,
    CONSTRAINT pk_usuarios PRIMARY KEY (id_usuario),
    CONSTRAINT uq_usuarios_nombre_usuario UNIQUE (nombre_usuario)
) COMMENT = 'Tabla de usuarios del sistema';
