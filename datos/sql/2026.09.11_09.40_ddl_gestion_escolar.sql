-- Script DDL principal para Gestión Escolar (basado en el diagrama UML)
-- Las tablas se crean en orden: primero las que no dependen de otras.
CREATE DATABASE IF NOT EXISTS gestion_escolar CHARACTER SET utf8mb4;
USE gestion_escolar;

CREATE TABLE periodos_academicos(
    id_periodo INTEGER AUTO_INCREMENT,
    anio INTEGER NOT NULL,
    semestre INTEGER NOT NULL,
    estado VARCHAR(30) NOT NULL,
    CONSTRAINT pk_periodos_academicos PRIMARY KEY (id_periodo),
    CONSTRAINT ck_periodos_semestre CHECK (semestre IN (1, 2)),
    CONSTRAINT ck_periodos_estado CHECK (estado IN ('Activo', 'Cerrado', 'Inactivo'))
) COMMENT = 'Tabla de periodos academicos';

CREATE TABLE docentes(
    id_docente INTEGER AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NULL,
    especialidad VARCHAR(100) NULL,
    CONSTRAINT pk_docentes PRIMARY KEY (id_docente)
) COMMENT = 'Tabla de docentes';

CREATE TABLE cursos(
    id_curso INTEGER AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL,
    nivel INTEGER NOT NULL,
    jornada VARCHAR(30) NOT NULL,
    id_periodo INTEGER NULL,
    CONSTRAINT pk_cursos PRIMARY KEY (id_curso),
    CONSTRAINT fk_cursos_periodos FOREIGN KEY (id_periodo) REFERENCES periodos_academicos(id_periodo)
) COMMENT = 'Tabla de cursos';

CREATE TABLE asignaturas(
    id_asignatura INTEGER AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL,
    codigo VARCHAR(20) NOT NULL,
    horasSemanales INTEGER NOT NULL,
    id_docente INTEGER NULL,
    id_curso INTEGER NULL,
    CONSTRAINT pk_asignaturas PRIMARY KEY (id_asignatura),
    CONSTRAINT ck_asignaturas_horas CHECK (horasSemanales > 0),
    CONSTRAINT fk_asignaturas_docentes FOREIGN KEY (id_docente) REFERENCES docentes(id_docente),
    CONSTRAINT fk_asignaturas_cursos FOREIGN KEY (id_curso) REFERENCES cursos(id_curso)
) COMMENT = 'Tabla de asignaturas';

-- UML: un apoderado puede tener varios estudiantes (1 a *).
-- Por eso la clave foránea va en estudiantes y no en apoderados.
CREATE TABLE apoderados(
    id_apoderado INTEGER AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    rut VARCHAR(15) NOT NULL UNIQUE,
    telefono VARCHAR(20) NULL,
    CONSTRAINT pk_apoderados PRIMARY KEY (id_apoderado)
) COMMENT = 'Tabla de apoderados';

CREATE TABLE estudiantes(
    id_estudiante INTEGER AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    rut VARCHAR(15) NOT NULL UNIQUE,
    fecha_nacimiento DATE NULL,
    id_curso INTEGER NULL,
    id_apoderado INTEGER NULL,
    CONSTRAINT pk_estudiantes PRIMARY KEY (id_estudiante),
    CONSTRAINT fk_estudiantes_cursos FOREIGN KEY (id_curso) REFERENCES cursos(id_curso),
    CONSTRAINT fk_estudiantes_apoderados FOREIGN KEY (id_apoderado) REFERENCES apoderados(id_apoderado)
) COMMENT = 'Tabla de estudiantes';

CREATE TABLE evaluaciones(
    id_evaluacion INTEGER AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    fecha DATE NULL,
    porcentaje DECIMAL(5,2) NOT NULL,
    id_asignatura INTEGER NULL,
    CONSTRAINT pk_evaluaciones PRIMARY KEY (id_evaluacion),
    CONSTRAINT ck_evaluaciones_porcentaje CHECK (porcentaje > 0 AND porcentaje <= 100),
    CONSTRAINT fk_evaluaciones_asignaturas FOREIGN KEY (id_asignatura) REFERENCES asignaturas(id_asignatura)
) COMMENT = 'Tabla de evaluaciones';

CREATE TABLE asistencias(
    id_asistencia INTEGER AUTO_INCREMENT,
    fecha DATE NOT NULL,
    presente TINYINT(1) NOT NULL DEFAULT 1,
    observacion VARCHAR(255) NULL,
    id_estudiante INTEGER NULL,
    CONSTRAINT pk_asistencias PRIMARY KEY (id_asistencia),
    CONSTRAINT fk_asistencias_estudiantes FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id_estudiante)
) COMMENT = 'Tabla de asistencias';

CREATE TABLE calificaciones(
    id_calificacion INTEGER AUTO_INCREMENT,
    nota DECIMAL(2,1) NOT NULL,
    fechaRegistro DATE NULL,
    observacion VARCHAR(255) NULL,
    id_estudiante INTEGER NULL,
    id_evaluacion INTEGER NULL,
    CONSTRAINT pk_calificaciones PRIMARY KEY (id_calificacion),
    CONSTRAINT ck_calificaciones_nota CHECK (nota BETWEEN 1.0 AND 7.0),
    CONSTRAINT fk_calificaciones_estudiantes FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id_estudiante),
    CONSTRAINT fk_calificaciones_evaluaciones FOREIGN KEY (id_evaluacion) REFERENCES evaluaciones(id_evaluacion)
) COMMENT = 'Tabla de calificaciones';

-- monto en pesos chilenos: entero, sin los errores de redondeo de FLOAT
CREATE TABLE pagos(
    id_pago INTEGER AUTO_INCREMENT,
    monto INTEGER NOT NULL,
    estado VARCHAR(30) NOT NULL,
    id_apoderado INTEGER NULL,
    CONSTRAINT pk_pagos PRIMARY KEY (id_pago),
    CONSTRAINT ck_pagos_monto CHECK (monto > 0),
    CONSTRAINT fk_pagos_apoderados FOREIGN KEY (id_apoderado) REFERENCES apoderados(id_apoderado)
) COMMENT = 'Tabla de pagos';
