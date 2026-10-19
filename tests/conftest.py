"""Configuración de las pruebas.

Las pruebas de negocio usan una base de datos SQLite en memoria (viene con Python)
en lugar de MySQL. Así se pueden ejecutar en cualquier equipo, sin .env y sin
tocar la base de datos real.
"""
from datetime import date

import pytest
from peewee import SqliteDatabase

from datos.modelos import MODELOS, PeriodoAcademico, Curso, Docente, Estudiante


@pytest.fixture
def base_prueba():
    """Base de datos vacía en memoria, con algunos datos como los de los scripts SQL."""
    base = SqliteDatabase(':memory:', pragmas={'foreign_keys': 1})
    # bind_ctx conecta los modelos a esta base solo mientras dura la prueba
    with base.bind_ctx(MODELOS):
        base.create_tables(MODELOS)
        periodo = PeriodoAcademico.create(anio=2026, semestre=2, estado='Activo')
        curso = Curso.create(nombre='1° Medio A', nivel=1, jornada='Mañana', periodo=periodo)
        Docente.create(nombre='Carlos Pérez', correo='carlos.perez@colegio.cl',
                       especialidad='Matemáticas')
        Estudiante.create(nombre='Cristopher Lagos', rut='21123456-3',
                          fecha_nacimiento=date(2008, 5, 15), curso=curso)
        yield base
    base.close()
