-- Modificación de tabla estudiantes: eliminación lógica (1 = activo, 0 = eliminado)
ALTER TABLE estudiantes ADD COLUMN activo TINYINT(1) NOT NULL DEFAULT 1;
