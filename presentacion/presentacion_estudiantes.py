from prettytable import PrettyTable
from negocio.negocio_estudiantes import (
    cargar_estudiantes, buscar_estudiantes, obtener_estudiante,
    crear_estudiante, actualizar_estudiante as actualizar_en_negocio,
    eliminar_estudiante as eliminar_en_negocio)

# Esta capa solo pide datos y muestra resultados.
# Toda la lógica y las validaciones están en la capa de negocio.


def mostrar_estudiantes():
    print(cargar_estudiantes(PrettyTable()))


def datos_estudiante():
    rut = input('Ingrese RUT de Estudiante (ej: 12345678-9): ')
    nombre = input('Ingrese Nombre de Estudiante: ')
    fecha_nacimiento = input('Ingrese Fecha de Nacimiento (YYYY-MM-DD): ')
    _, mensaje = crear_estudiante(rut, nombre, fecha_nacimiento)
    print(mensaje)


def buscar_estudiante_nombre(nombre):
    print(buscar_estudiantes(PrettyTable(), nombre))


def _seleccionar_estudiante(accion):
    nombre_busqueda = input('Ingrese Nombre de Estudiante a buscar: ')
    buscar_estudiante_nombre(nombre_busqueda)
    id_ingresado = input(f'Ingrese Id de Estudiante para {accion}: ')
    estudiante = obtener_estudiante(id_ingresado)
    if estudiante is None:
        print('No se encontró un estudiante activo con ese Id.')
    return estudiante


def actualizar_estudiante():
    estudiante = _seleccionar_estudiante('modificar')
    if estudiante is not None:
        nombre_nuevo = input('Ingrese Nuevo Nombre (o ENTER para conservar): ')
        rut_nuevo = input('Ingrese Nuevo RUT (o ENTER para conservar): ')
        _, mensaje = actualizar_en_negocio(estudiante, nombre_nuevo, rut_nuevo)
        print(mensaje)


def eliminar_estudiante():
    estudiante = _seleccionar_estudiante('eliminar')
    if estudiante is not None:
        confirmacion = input(f'¿Seguro que desea eliminar a {estudiante.nombre}? (s/n): ')
        if confirmacion.strip().lower() == 's':
            _, mensaje = eliminar_en_negocio(estudiante)
            print(mensaje)
        else:
            print('Operación cancelada.')
