from peewee import PeeweeException
from datos.modelos import Curso
from datos.auxiliar import registrar_error


def listado_cursos():
    try:
        return list(Curso.select())
    except PeeweeException as error:
        registrar_error(error)
        return []


def guardar_curso(nombre, nivel, jornada, periodo=None):
    try:
        return Curso.create(nombre=nombre, nivel=nivel, jornada=jornada, periodo=periodo)
    except PeeweeException as error:
        registrar_error(error)
        return None
