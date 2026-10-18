from negocio.negocio_estudiantes import cargar_estudiantes, crear_estudiante, buscar_estudiantes
from datos.repositorio.repositorio_estudiantes import estudiante_por_id, guardar_estudiante, estudiante_por_nombre_exacto
from datos.models import Estudiantes
from prettytable import PrettyTable

def mostrar_estudiantes():
    tabla_estudiantes = PrettyTable()
    tabla_estudiantes = cargar_estudiantes(tabla_estudiantes)
    print(tabla_estudiantes)

def datos_estudiante():
    rut = input('Ingrese RUT de Estudiante: ')
    nombre = input('Ingrese Nombre de Estudiante: ')
    fecha_nacimiento = input('Ingrese Fecha de Nacimiento (YYYY-MM-DD): ')
    crear_estudiante(rut, nombre.title(), fecha_nacimiento)

def buscar_estudiante_nombre(nombre):
    tabla_estudiantes = PrettyTable()
    tabla_estudiantes = buscar_estudiantes(tabla_estudiantes, nombre)
    print(tabla_estudiantes)

def actualizar_estudiante():
    nombre_busqueda = input('Ingrese Nombre de Estudiante a buscar: ')
    buscar_estudiante_nombre(nombre_busqueda)
    id_ingresado = input('Ingrese Id de Estudiante para modificar: ')
    estudiante = estudiante_por_id(id_ingresado)
    if estudiante:
        nombre_nuevo = input('Ingrese Nuevo Nombre de Estudiante (o ENTER para conservar): ')
        rut_nuevo = input('Ingrese Nuevo RUT de Estudiante (o ENTER para conservar): ')
        
        if nombre_nuevo != '':
            estudiante.nombre = nombre_nuevo.title()
        if rut_nuevo != '':
            estudiante.rut = rut_nuevo
            
        respuesta = guardar_estudiante(estudiante)
        if respuesta == 1:
            print(f'Estudiante {estudiante.nombre} actualizado con éxito')
    else:
        print('Estudiante no encontrado con ese ID.')

def eliminar_estudiante():
    nombre_busqueda = input('Ingrese Nombre de Estudiante: ')
    buscar_estudiante_nombre(nombre_busqueda)
    id_ingresado = input('Ingrese Id de Estudiante para eliminar: ')
    estudiante = estudiante_por_id(id_ingresado)
    if estudiante:
        # En el modelo podemos marcar inhabilitado o eliminar físicamente según prefiera
        respuesta = guardar_estudiante(estudiante)
        if respuesta == 1:
            print(f'Estudiante {estudiante.nombre} procesado con éxito')
    else:
        print('Estudiante no encontrado.')
