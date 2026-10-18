from peewee import PeeweeException
from datos.modelos import Estudiante
from datos.auxiliar import registrar_error

# Nota: en Peewee, select() no ejecuta la consulta hasta que se recorre.
# Por eso usamos list(...) DENTRO del try: así un error de la base de datos
# se captura aquí y no explota después en otra capa.


def listado_estudiantes():
    try:
        return list(Estudiante.select().where(Estudiante.activo == True))
    except PeeweeException as error:
        registrar_error(error)
        return []


def estudiante_por_nombre(nombre):
    try:
        return list(Estudiante.select().where(
            (Estudiante.nombre.contains(nombre)) & (Estudiante.activo == True)))
    except PeeweeException as error:
        registrar_error(error)
        return []


def estudiante_por_id(id_estudiante):
    try:
        return Estudiante.get_or_none(
            (Estudiante.id_estudiante == id_estudiante) & (Estudiante.activo == True))
    except PeeweeException as error:
        registrar_error(error)
        return None


def existe_rut(rut, excluir_id=None):
    """Indica si el RUT ya está registrado (opcionalmente ignorando un id)."""
    try:
        consulta = Estudiante.select().where(Estudiante.rut == rut)
        if excluir_id is not None:
            consulta = consulta.where(Estudiante.id_estudiante != excluir_id)
        return consulta.exists()
    except PeeweeException as error:
        registrar_error(error)
        return False


def guardar_estudiante(estudiante: Estudiante):
    try:
        estudiante.save()
        return True
    except PeeweeException as error:
        registrar_error(error)
        return False
