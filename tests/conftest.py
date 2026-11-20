"""Configuración de las pruebas.

Las pruebas de negocio usan una base de datos SQLite en memoria (viene con Python)
en lugar de MySQL. Así se pueden ejecutar en cualquier equipo, sin .env y sin
tocar la base de datos real.
"""
from datetime import date

import pytest
from peewee import SqliteDatabase

from datos.auxiliares import seguridad
from datos.modelos import MODELOS, PeriodoAcademico, Curso, Docente, Estudiante


@pytest.fixture(autouse=True)
def bcrypt_rapido(monkeypatch):
    """bcrypt con costo 12 tarda ~0,3 s por hash; con costo 4 (el mínimo), milisegundos.
    El algoritmo es el mismo, solo cambia cuántas vueltas da. Se aplica a todas las pruebas."""
    monkeypatch.setattr(seguridad, 'COSTO', 4)


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
