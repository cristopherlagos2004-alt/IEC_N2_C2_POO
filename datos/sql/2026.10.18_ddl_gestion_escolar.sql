-- Script DDL de creación de base de datos y tablas para Gestión Escolar
-- Basado en el diagrama UML de gestión escolar

CREATE DATABASE IF NOT EXISTS gestion_escolar;
USE gestion_escolar;

-- Tabla: periodicos_academicos
CREATE TABLE periodicos_academicos(
    id_periodico INTEGER AUTO_INCREMENT,
    anio INTEGER NOT NULL,
    semestre INTEGER NOT NULL,
    estado VARCHAR(30) NOT NULL,
    
    CONSTRAINT pk_periodicos_academicos PRIMARY KEY (id_periodico)
) COMMENT = 'Tabla de periodos académicos del colegio';

-- Tabla: docentes
CREATE TABLE docentes(
    id_docente INTEGER AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NULL,
    especialidad VARCHAR(100) NULL,
    
    CONSTRAINT pk_docentes PRIMARY KEY (id_docente)
) COMMENT = 'Tabla de profesores e instructores';

-- Tabla: cursos
CREATE TABLE cursos(
    id_curso INTEGER AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL,
    nivel INTEGER NOT NULL,
    jornada VARCHAR(30) NOT NULL,
    id_periodico INTEGER NULL,
    
    CONSTRAINT pk_cursos PRIMARY KEY (id_curso),
    CONSTRAINT fk_cursos_periodicos FOREIGN KEY (id_periodico) REFERENCES periodicos_academicos(id_periodico)
) COMMENT = 'Tabla de cursos y niveles académicos';

-- Tabla: asignaturas
CREATE TABLE asignaturas(
    id_asignatura INTEGER AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL,
    codigo VARCHAR(20) NOT NULL,
    horasSemanales INTEGER NOT NULL,
    id_docente INTEGER NULL,
    id_curso INTEGER NULL,
    
    CONSTRAINT pk_asignaturas PRIMARY KEY (id_asignatura),
    CONSTRAINT fk_asignaturas_docentes FOREIGN KEY (id_docente) REFERENCES docentes(id_docente),
    CONSTRAINT fk_asignaturas_cursos FOREIGN KEY (id_curso) REFERENCES cursos(id_curso)
) COMMENT = 'Tabla de materias y asignaturas';

-- Tabla: estudiantes
CREATE TABLE estudiantes(
    id_estudiante INTEGER AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    rut VARCHAR(15) NOT NULL UNIQUE,
    fecha_nacimiento DATE NULL,
    id_curso INTEGER NULL,
    
    CONSTRAINT pk_estudiantes PRIMARY KEY (id_estudiante),
    CONSTRAINT fk_estudiantes_cursos FOREIGN KEY (id_curso) REFERENCES cursos(id_curso)
) COMMENT = 'Tabla de estudiantes matriculados';

-- Tabla: evaluaciones
CREATE TABLE evaluaciones(
    id_evaluacion INTEGER AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    fecha DATE NULL,
    porcentaje FLOAT NOT NULL,
    id_asignatura INTEGER NULL,
    
    CONSTRAINT pk_evaluaciones PRIMARY KEY (id_evaluacion),
    CONSTRAINT fk_evaluaciones_asignaturas FOREIGN KEY (id_asignatura) REFERENCES asignaturas(id_asignatura)
) COMMENT = 'Tabla de pruebas y evaluaciones';

-- Tabla: apoderados
CREATE TABLE apoderados(
    id_apoderado INTEGER AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    rut VARCHAR(15) NOT NULL UNIQUE,
    telefono VARCHAR(20) NULL,
    id_estudiante INTEGER NULL,
    
    CONSTRAINT pk_apoderados PRIMARY KEY (id_apoderado),
    CONSTRAINT fk_apoderados_estudiantes FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id_estudiante)
) COMMENT = 'Tabla de apoderados y tutores legales';

-- Tabla: asistencias
CREATE TABLE asistencias(
    id_asistencia INTEGER AUTO_INCREMENT,
    fecha DATE NOT NULL,
    presente TINYINT NOT NULL DEFAULT 1,
    observacion VARCHAR(255) NULL,
    id_estudiante INTEGER NULL,
    
    CONSTRAINT pk_asistencias PRIMARY KEY (id_asistencia),
    CONSTRAINT fk_asistencias_estudiantes FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id_estudiante)
) COMMENT = 'Registro diario de asistencia de alumnos';

-- Tabla: calificaciones
CREATE TABLE calificaciones(
    id_calificacion INTEGER AUTO_INCREMENT,
    nota FLOAT NOT NULL,
    fechaRegistro DATE NULL,
    observacion VARCHAR(255) NULL,
    id_estudiante INTEGER NULL,
    id_evaluacion INTEGER NULL,
    
    CONSTRAINT pk_calificaciones PRIMARY KEY (id_calificacion),
    CONSTRAINT fk_calificaciones_estudiantes FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id_estudiante),
    CONSTRAINT fk_calificaciones_evaluaciones FOREIGN KEY (id_evaluacion) REFERENCES evaluaciones(id_evaluacion)
) COMMENT = 'Registro de notas de estudiantes por evaluacion';

-- Tabla: pagos
CREATE TABLE pagos(
    id_pago INTEGER AUTO_INCREMENT,
    monto FLOAT NOT NULL,
    estado VARCHAR(30) NOT NULL,
    id_apoderado INTEGER NULL,
    
    CONSTRAINT pk_pagos PRIMARY KEY (id_pago),
    CONSTRAINT fk_pagos_apoderados FOREIGN KEY (id_apoderado) REFERENCES apoderados(id_apoderado)
) COMMENT = 'Registro de colegiaturas y pagos de apoderados';
