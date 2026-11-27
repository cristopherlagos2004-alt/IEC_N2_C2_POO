"""Repositorio de evaluaciones: funciones para guardar y consultar la tabla evaluaciones."""
from peewee import fn
from datos.modelos import Evaluacion
from datos.repositorio import repositorio_base as base
from datos.repositorio.repositorio_base import ejecutar  # noqa: F401  (la capa de negocio también la usa)

# Modelo que maneja este repositorio (la capa de negocio lo usa para crear registros)
modelo = Evaluacion


def guardar(evaluacion):
    """Inserta la evaluación si es nuevo, o lo actualiza si ya existe, usando save()."""
    ejecutar(lambda: evaluacion.save())


def listar():
    """Todos los evaluaciones, ordenados por Id."""
    return base.listar(Evaluacion)


def obtener_por_id(id_evaluacion):
    """La evaluación con ese Id, o None si no existe."""
    return base.obtener_por_id(Evaluacion, id_evaluacion)


def buscar(texto):
    """Evaluaciones cuyo nombre contiene el texto."""
    return base.buscar(Evaluacion, Evaluacion.nombre.contains(texto))


def eliminar(evaluacion):
    """Borra la evaluación de la tabla."""
    base.eliminar(evaluacion)


def contar_dependencias(evaluacion):
    """Registros de otras tablas que dependen de la evaluación (para avisar antes de eliminar)."""
    return base.contar_dependencias(Evaluacion, evaluacion)


def suma_porcentajes(asignatura, excluir_id=None):
    """Suma de las ponderaciones de las evaluaciones de una asignatura."""
    consulta = (Evaluacion.select(fn.COALESCE(fn.SUM(Evaluacion.porcentaje), 0))
                .where(Evaluacion.asignatura == asignatura))
    if excluir_id is not None:
        consulta = consulta.where(Evaluacion.id_evaluacion != excluir_id)
    return ejecutar(consulta.scalar)
