"""Repositorio de cursos: funciones para guardar y consultar la tabla cursos."""
from datos.modelos import Curso
from datos.repositorio import repositorio_base as base
from datos.repositorio.repositorio_base import ejecutar  # noqa: F401  (la capa de negocio también la usa)

# Modelo que maneja este repositorio (la capa de negocio lo usa para crear registros)
modelo = Curso


def guardar(curso):
    """Inserta el curso si es nuevo, o lo actualiza si ya existe, usando save()."""
    ejecutar(lambda: curso.save())


def listar():
    """Todos los cursos, ordenados por Id."""
    return base.listar(Curso)


def obtener_por_id(id_curso):
    """El curso con ese Id, o None si no existe."""
    return base.obtener_por_id(Curso, id_curso)


def buscar(texto):
    """Cursos cuyo nombre contiene el texto."""
    return base.buscar(Curso, Curso.nombre.contains(texto))


def eliminar(curso):
    """Borra el curso de la tabla."""
    base.eliminar(curso)


def contar_dependencias(curso):
    """Registros de otras tablas que dependen de el curso (para avisar antes de eliminar)."""
    return base.contar_dependencias(Curso, curso)


def existe_nombre(nombre, periodo, excluir_id=None):
    """True si ya hay un curso con ese nombre en el mismo periodo."""
    return base.existe(Curso, (Curso.nombre == nombre) & (Curso.periodo == periodo), excluir_id)
