import sys
from datos import nombre_app, version_app, main_menu
from presentacion.presentacion_estudiantes import mostrar_estudiantes, datos_estudiante, buscar_estudiante_nombre, actualizar_estudiante, eliminar_estudiante

def menu_principal():
    print(f'{nombre_app} {version_app}')
    print('='*len(nombre_app) + "=" + '='*len(version_app))

    while True:
        for clave, valor in main_menu.items():
            print(f'[{clave}] - {valor}')

        opcion_usuario = input('Ingrese una opción [1-5]: ')

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
            print('Saliendo de Sistema')
            sys.exit()
        else:
            print('Opción Ingresada NO corresponde...\nIngrese nuevamente.')
