"""Repositorio de pagos: funciones para guardar y consultar la tabla pagos."""
from datos.modelos import Pago, Apoderado
from datos.repositorio import repositorio_base as base
from datos.repositorio.repositorio_base import ejecutar  # noqa: F401  (la capa de negocio también la usa)

# Modelo que maneja este repositorio (la capa de negocio lo usa para crear registros)
modelo = Pago


def guardar(pago):
    """Inserta el pago si es nuevo, o lo actualiza si ya existe, usando save()."""
    ejecutar(lambda: pago.save())


def listar():
    """Todos los pagos, ordenados por Id."""
    return base.listar(Pago)


def obtener_por_id(id_pago):
    """El pago con ese Id, o None si no existe."""
    return base.obtener_por_id(Pago, id_pago)


def buscar(texto):
    """Pagos de los apoderados cuyo nombre contiene el texto."""
    return base.buscar(Pago, Apoderado.nombre.contains(texto), Pago.select().join(Apoderado))


def eliminar(pago):
    """Borra el pago de la tabla."""
    base.eliminar(pago)


def contar_dependencias(pago):
    """Registros de otras tablas que dependen de el pago (para avisar antes de eliminar)."""
    return base.contar_dependencias(Pago, pago)
