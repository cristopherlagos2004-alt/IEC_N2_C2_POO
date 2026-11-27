-- Evaluación 3: usuario inicial para poder entrar al sistema la primera vez.
--   Usuario:    admin
--   Contraseña: Admin2026!
-- La contraseña se guarda como hash BCrypt (costo 12), nunca en texto plano.
-- IMPORTANTE: después del primer ingreso, cambie esta contraseña desde
-- el menú "Usuarios" -> "Cambiar contraseña".
USE gestion_escolar;

INSERT INTO usuarios (nombre_usuario, nombre, clave_hash, activo)
VALUES ('admin', 'Administrador', '$2b$12$RVsUHZteV6nbplYOlKTuq.cpUPBSTPbgKlsHXjuSQ0qFBlkhcKPO6', 1);
