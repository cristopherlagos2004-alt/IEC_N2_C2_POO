from datos.conexion import base_datos
from datos.models import Estudiantes
from datos.auxiliar import mensaje_error_orm

database = base_datos()

def listado_estudiantes():
    try:
        return Estudiantes.select()
    except Exception as error:
        print(f"{mensaje_error_orm} {error}")
        return []

def guardar_estudiante(estudiante: Estudiantes):
    try:
        estudiante.save()
        return 1
    except Exception as error:
        print(f"{mensaje_error_orm} {error}")
        return 0

def estudiante_por_nombre(nombre):
    try:
        estudiantes = Estudiantes.select().where(Estudiantes.nombre.contains(nombre))
        return estudiantes
    except Exception as error:
        print(f"{mensaje_error_orm} {error}")
        return []

def estudiante_por_id(id_est):
    try:
        return Estudiantes.get_by_id(id_est)
    except Exception as error:
        print(f"{mensaje_error_orm} {error}")
        return None

def estudiante_por_nombre_exacto(nombre):
    try:
        return Estudiantes.select().where(Estudiantes.nombre == nombre)
    except Exception as error:
        print(f"{mensaje_error_orm} {error}")
        return []
