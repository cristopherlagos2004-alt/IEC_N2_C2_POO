-- Inserción de Periodos Académicos
-- (se ejecuta antes que los cursos, porque los cursos apuntan a un periodo)
INSERT INTO periodos_academicos (anio, semestre, estado) VALUES
(2026, 1, 'Cerrado'),
(2026, 2, 'Activo'),
(2027, 1, 'Inactivo');
