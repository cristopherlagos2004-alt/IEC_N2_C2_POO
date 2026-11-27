"""Repositorio de asignaturas: funciones para guardar y consultar la tabla asignaturas."""
from datos.modelos import Asignatura
from datos.repositorio import repositorio_base as base
from datos.repositorio.repositorio_base import ejecutar  # noqa: F401  (la capa de negocio también la usa)

# Modelo que maneja este repositorio (la capa de negocio lo usa para crear registros)
modelo = Asignatura


def guardar(asignatura):
    """Inserta la asignatura si es nuevo, o lo actualiza si ya existe, usando save()."""
    ejecutar(lambda: asignatura.save())


def listar():
    """Todos los asignaturas, ordenados por Id."""
    return base.listar(Asignatura)


def obtener_por_id(id_asignatura):
    """La asignatura con ese Id, o None si no existe."""
    return base.obtener_por_id(Asignatura, id_asignatura)


def buscar(texto):
    """Asignaturas cuyo nombre o código contiene el texto."""
    return base.buscar(Asignatura, Asignatura.nombre.contains(texto) |
                       Asignatura.codigo.contains(texto))


def eliminar(asignatura):
    """Borra la asignatura de la tabla."""
    base.eliminar(asignatura)


def contar_dependencias(asignatura):
    """Registros de otras tablas que dependen de la asignatura (para avisar antes de eliminar)."""
    return base.contar_dependencias(Asignatura, asignatura)


def existe_codigo(codigo, curso, excluir_id=None):
    """True si ya hay una asignatura con ese código en el mismo curso."""
    return base.existe(Asignatura, (Asignatura.codigo == codigo) & (Asignatura.curso == curso),
                       excluir_id)
