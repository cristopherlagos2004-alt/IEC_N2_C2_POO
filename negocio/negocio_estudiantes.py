from datos.repositorio.repositorio_estudiantes import listado_estudiantes, guardar_estudiante, estudiante_por_nombre
from prettytable import PrettyTable
from datos.models import Estudiantes

def cargar_estudiantes(tabla: PrettyTable):
    estudiantes = listado_estudiantes()
    tabla.field_names = ['Id', 'RUT', 'Nombre', 'Fecha Nacimiento']
    if estudiantes:
        for est in estudiantes:
            tabla.add_row([est.id_estudiante, est.rut, est.nombre, est.fecha_nacimiento])
    return tabla

def buscar_estudiantes(tabla: PrettyTable, nombre):
    estudiantes = estudiante_por_nombre(nombre)
    tabla.field_names = ['Id', 'RUT', 'Nombre', 'Fecha Nacimiento']
    if estudiantes:
        for est in estudiantes:
            tabla.add_row([est.id_estudiante, est.rut, est.nombre, est.fecha_nacimiento])
    return tabla

def crear_estudiante(rut, nombre, fecha_nacimiento):
    nuevo_estudiante = Estudiantes()
    nuevo_estudiante.rut = rut
    nuevo_estudiante.nombre = nombre
    nuevo_estudiante.fecha_nacimiento = fecha_nacimiento
    resultado = guardar_estudiante(nuevo_estudiante)
    if resultado == 1:
        print(f"Se ha guardado el estudiante {nuevo_estudiante.nombre} con RUT: {nuevo_estudiante.rut}")
