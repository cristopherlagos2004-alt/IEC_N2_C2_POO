from prettytable import PrettyTable
from datos.modelos import Estudiante
from datos.repositorio.repositorio_estudiantes import (
    listado_estudiantes, estudiante_por_nombre, estudiante_por_id,
    existe_rut, guardar_estudiante)
from negocio.validaciones import validar_rut, validar_nombre, validar_fecha_nacimiento

COLUMNAS = ['Id', 'RUT', 'Nombre', 'Fecha Nacimiento']


def _llenar_tabla(tabla: PrettyTable, estudiantes):
    tabla.field_names = COLUMNAS
    for est in estudiantes:
        tabla.add_row([est.id_estudiante, est.rut, est.nombre, est.fecha_nacimiento])
    return tabla


def cargar_estudiantes(tabla: PrettyTable):
    return _llenar_tabla(tabla, listado_estudiantes())


def buscar_estudiantes(tabla: PrettyTable, nombre):
    return _llenar_tabla(tabla, estudiante_por_nombre(nombre.strip()))


def obtener_estudiante(id_texto):
    """Devuelve el estudiante activo con ese id, o None si el id no es válido."""
    if not id_texto.strip().isdigit():
        return None
    return estudiante_por_id(int(id_texto))


def crear_estudiante(rut, nombre, fecha_nacimiento):
    """Valida y guarda. Devuelve (exito, mensaje)."""
    try:
        rut = validar_rut(rut)
        nombre = validar_nombre(nombre)
        fecha = validar_fecha_nacimiento(fecha_nacimiento)
    except ValueError as error:
        return False, str(error)

    if existe_rut(rut):
        return False, f'Ya existe un estudiante con RUT {rut}.'

    nuevo = Estudiante(rut=rut, nombre=nombre, fecha_nacimiento=fecha)
    if guardar_estudiante(nuevo):
        return True, f'Se guardó el estudiante {nombre} con RUT {rut}.'
    return False, 'No se pudo guardar el estudiante.'


def actualizar_estudiante(estudiante: Estudiante, nombre_nuevo='', rut_nuevo=''):
    """Cambia solo los campos que vengan con texto. Devuelve (exito, mensaje)."""
    if not nombre_nuevo.strip() and not rut_nuevo.strip():
        return False, 'No se ingresaron cambios.'
    try:
        if nombre_nuevo.strip():
            estudiante.nombre = validar_nombre(nombre_nuevo)
        if rut_nuevo.strip():
            rut = validar_rut(rut_nuevo)
            if existe_rut(rut, excluir_id=estudiante.id_estudiante):
                return False, f'El RUT {rut} ya pertenece a otro estudiante.'
            estudiante.rut = rut
    except ValueError as error:
        return False, str(error)

    if guardar_estudiante(estudiante):
        return True, f'Estudiante {estudiante.nombre} actualizado con éxito.'
    return False, 'No se pudo actualizar el estudiante.'


def eliminar_estudiante(estudiante: Estudiante):
    """Eliminación lógica: marca al estudiante como inactivo."""
    estudiante.activo = False
    if guardar_estudiante(estudiante):
        return True, f'Estudiante {estudiante.nombre} eliminado (desactivado) con éxito.'
    return False, 'No se pudo eliminar el estudiante.'
