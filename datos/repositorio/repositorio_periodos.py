"""Repositorio de periodos: funciones para guardar y consultar la tabla periodos_academicos."""
from datos.modelos import PeriodoAcademico
from datos.repositorio import repositorio_base as base
from datos.repositorio.repositorio_base import ejecutar  # noqa: F401  (la capa de negocio también la usa)

# Modelo que maneja este repositorio (la capa de negocio lo usa para crear registros)
modelo = PeriodoAcademico


def guardar(periodo):
    """Inserta el periodo si es nuevo, o lo actualiza si ya existe, usando save()."""
    ejecutar(lambda: periodo.save())


def listar():
    """Todos los periodos, ordenados por Id."""
    return base.listar(PeriodoAcademico)


def obtener_por_id(id_periodo):
    """El periodo con ese Id, o None si no existe."""
    return base.obtener_por_id(PeriodoAcademico, id_periodo)


def buscar(texto):
    """Los periodos no tienen nombre: se buscan por año (si es un número) o por estado."""
    if texto.isdigit():
        return base.buscar(PeriodoAcademico, PeriodoAcademico.anio == int(texto))
    return base.buscar(PeriodoAcademico, PeriodoAcademico.estado.contains(texto))


def eliminar(periodo):
    """Borra el periodo de la tabla."""
    base.eliminar(periodo)


def contar_dependencias(periodo):
    """Registros de otras tablas que dependen de el periodo (para avisar antes de eliminar)."""
    return base.contar_dependencias(PeriodoAcademico, periodo)


def existe_periodo(anio, semestre, excluir_id=None):
    return base.existe(PeriodoAcademico, (PeriodoAcademico.anio == anio) &
                       (PeriodoAcademico.semestre == semestre), excluir_id)


def existe_otro_activo(excluir_id=None):
    return base.existe(PeriodoAcademico, PeriodoAcademico.estado == 'Activo', excluir_id)
