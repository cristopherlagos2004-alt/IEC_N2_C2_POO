from datos.auxiliar import nombre_app, version_app, main_menu
from presentacion.menu_autor import solicitar_datos_autor
from presentacion.presentacion_estudiantes import (
    mostrar_estudiantes, datos_estudiante, buscar_estudiante_nombre,
    actualizar_estudiante, eliminar_estudiante)


def menu_principal():
    titulo = f'{nombre_app} {version_app}'
    print(titulo)
    print('=' * len(titulo))
    solicitar_datos_autor()

    while True:
        print()
        for clave, valor in main_menu.items():
            print(f'[{clave}] - {valor}')

        opcion_usuario = input(f'Ingrese una opción [1-{len(main_menu)}]: ').strip()

        if opcion_usuario == '1':
            mostrar_estudiantes()
        elif opcion_usuario == '2':
            datos_estudiante()
        elif opcion_usuario == '3':
            nombre_buscar = input('Ingrese nombre a buscar: ')
            buscar_estudiante_nombre(nombre_buscar)
        elif opcion_usuario == '4':
            actualizar_estudiante()
        elif opcion_usuario == '5':
            eliminar_estudiante()
        elif opcion_usuario == '6':
            print('Saliendo del Sistema')
            break
        else:
            print('Opción ingresada NO corresponde. Ingrese nuevamente.')
