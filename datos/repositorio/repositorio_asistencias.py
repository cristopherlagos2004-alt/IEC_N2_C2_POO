"""Repositorio de asistencias: funciones para guardar y consultar la tabla asistencias."""
from datos.modelos import Asistencia, Estudiante
from datos.repositorio import repositorio_base as base
from datos.repositorio.repositorio_base import ejecutar  # noqa: F401  (la capa de negocio también la usa)

# Modelo que maneja este repositorio (la capa de negocio lo usa para crear registros)
modelo = Asistencia


def guardar(asistencia):
    """Inserta la asistencia si es nuevo, o lo actualiza si ya existe, usando save()."""
    ejecutar(lambda: asistencia.save())


def listar():
    """Todos los asistencias, ordenados por Id."""
    return base.listar(Asistencia)


def obtener_por_id(id_asistencia):
    """La asistencia con ese Id, o None si no existe."""
    return base.obtener_por_id(Asistencia, id_asistencia)


def buscar(texto):
    """Asistencias de los estudiantes cuyo nombre contiene el texto."""
    return ejecutar(lambda: list(
        Asistencia.select().join(Estudiante)
        .where(Estudiante.nombre.contains(texto))
        .order_by(Asistencia.fecha, Asistencia.id_asistencia)))


def eliminar(asistencia):
    """Borra la asistencia de la tabla."""
    base.eliminar(asistencia)


def contar_dependencias(asistencia):
    """Registros de otras tablas que dependen de la asistencia (para avisar antes de eliminar)."""
    return base.contar_dependencias(Asistencia, asistencia)


def existe_asistencia(estudiante, fecha, excluir_id=None):
    """Un estudiante tiene un solo registro de asistencia por día."""
    return base.existe(Asistencia, (Asistencia.estudiante == estudiante) &
                       (Asistencia.fecha == fecha), excluir_id)
