"""Repositorio de docentes: funciones para guardar y consultar la tabla docentes."""
from datos.modelos import Docente
from datos.repositorio import repositorio_base as base
from datos.repositorio.repositorio_base import ejecutar  # noqa: F401  (la capa de negocio también la usa)

# Modelo que maneja este repositorio (la capa de negocio lo usa para crear registros)
modelo = Docente


def guardar(docente):
    """Inserta el docente si es nuevo, o lo actualiza si ya existe, usando save()."""
    ejecutar(lambda: docente.save())


def listar():
    """Todos los docentes, ordenados por Id."""
    return base.listar(Docente)


def obtener_por_id(id_docente):
    """El docente con ese Id, o None si no existe."""
    return base.obtener_por_id(Docente, id_docente)


def buscar(texto):
    """Docentes cuyo nombre contiene el texto."""
    return base.buscar(Docente, Docente.nombre.contains(texto))


def eliminar(docente):
    """Borra el docente de la tabla."""
    base.eliminar(docente)


def contar_dependencias(docente):
    """Registros de otras tablas que dependen de el docente (para avisar antes de eliminar)."""
    return base.contar_dependencias(Docente, docente)
