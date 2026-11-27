"""Repositorio de calificaciones: funciones para guardar y consultar la tabla calificaciones."""
from datos.modelos import Calificacion, Estudiante
from datos.repositorio import repositorio_base as base
from datos.repositorio.repositorio_base import ejecutar  # noqa: F401  (la capa de negocio también la usa)

# Modelo que maneja este repositorio (la capa de negocio lo usa para crear registros)
modelo = Calificacion


def guardar(calificacion):
    """Inserta la calificación si es nuevo, o lo actualiza si ya existe, usando save()."""
    ejecutar(lambda: calificacion.save())


def listar():
    """Todos los calificaciones, ordenados por Id."""
    return base.listar(Calificacion)


def obtener_por_id(id_calificacion):
    """La calificación con ese Id, o None si no existe."""
    return base.obtener_por_id(Calificacion, id_calificacion)


def buscar(texto):
    """Calificaciones de los estudiantes cuyo nombre contiene el texto."""
    return base.buscar(Calificacion, Estudiante.nombre.contains(texto),
                       Calificacion.select().join(Estudiante))


def eliminar(calificacion):
    """Borra la calificación de la tabla."""
    base.eliminar(calificacion)


def contar_dependencias(calificacion):
    """Registros de otras tablas que dependen de la calificación (para avisar antes de eliminar)."""
    return base.contar_dependencias(Calificacion, calificacion)


def existe_calificacion(estudiante, evaluacion, excluir_id=None):
    """Un estudiante tiene una sola nota por evaluación."""
    return base.existe(Calificacion, (Calificacion.estudiante == estudiante) &
                       (Calificacion.evaluacion == evaluacion), excluir_id)
