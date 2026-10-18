from datos.conexion import base_datos
from datos.modelos.curso import Curso
from datos.auxiliar import mensaje_error_orm

database = base_datos()

def listado_cursos():
    try:
        return Curso.select()
    except Exception as error:
        print(f"{mensaje_error_orm} {error}")
        return []

def guardar_curso(nombre, nivel, jornada):
    try:
        return Curso.create(nombre=nombre, nivel=nivel, jornada=jornada)
    except Exception as error:
        print(f"{mensaje_error_orm} {error}")
