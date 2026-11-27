"""Repositorio de estudiantes: funciones para guardar y consultar la tabla estudiantes."""
from datos.modelos import Estudiante
from datos.repositorio import repositorio_base as base
from datos.repositorio.repositorio_base import ejecutar  # noqa: F401  (la capa de negocio también la usa)

# Modelo que maneja este repositorio (la capa de negocio lo usa para crear registros)
modelo = Estudiante


def guardar(estudiante):
    """Inserta el estudiante si es nuevo, o lo actualiza si ya existe, usando save()."""
    ejecutar(lambda: estudiante.save())


def listar():
    """Estudiantes activos, ordenados por Id."""
    return base.listar(Estudiante, _activos())


def obtener_por_id(id_estudiante):
    """El estudiante con ese Id, o None si no existe."""
    return base.obtener_por_id(Estudiante, id_estudiante, _activos())


def buscar(texto):
    """Estudiantes activos cuyo nombre contiene el texto."""
    return base.buscar(Estudiante, Estudiante.nombre.contains(texto), _activos())


def eliminar(estudiante):
    """Eliminación LÓGICA: no borra la fila (se conservan sus notas y asistencias),
    solo la marca como inactiva."""
    base.deshabilitar(estudiante)


def contar_dependencias(estudiante):
    return base.contar_dependencias(Estudiante, estudiante)


def existe_rut(rut, excluir_id=None):
    """Revisa TODOS los estudiantes, incluso los desactivados (el RUT es único)."""
    return base.existe(Estudiante, Estudiante.rut == rut, excluir_id)


def _activos():
    """Consulta de partida: solo los estudiantes activos."""
    return Estudiante.select().where(Estudiante.activo == True)  # noqa: E712
