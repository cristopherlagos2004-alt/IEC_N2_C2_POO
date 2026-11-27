"""Repositorio de apoderados: funciones para guardar y consultar la tabla apoderados."""
from datos.modelos import Apoderado
from datos.repositorio import repositorio_base as base
from datos.repositorio.repositorio_base import ejecutar  # noqa: F401  (la capa de negocio también la usa)

# Modelo que maneja este repositorio (la capa de negocio lo usa para crear registros)
modelo = Apoderado


def guardar(apoderado):
    """Inserta el apoderado si es nuevo, o lo actualiza si ya existe, usando save()."""
    ejecutar(lambda: apoderado.save())


def listar():
    """Todos los apoderados, ordenados por Id."""
    return base.listar(Apoderado)


def obtener_por_id(id_apoderado):
    """El apoderado con ese Id, o None si no existe."""
    return base.obtener_por_id(Apoderado, id_apoderado)


def buscar(texto):
    """Apoderados cuyo nombre contiene el texto."""
    return base.buscar(Apoderado, Apoderado.nombre.contains(texto))


def eliminar(apoderado):
    """Borra el apoderado de la tabla."""
    base.eliminar(apoderado)


def contar_dependencias(apoderado):
    """Registros de otras tablas que dependen de el apoderado (para avisar antes de eliminar)."""
    return base.contar_dependencias(Apoderado, apoderado)


def existe_rut(rut, excluir_id=None):
    """True si ya hay otro apoderado con ese RUT."""
    return base.existe(Apoderado, Apoderado.rut == rut, excluir_id)
