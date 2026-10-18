import sys
from decouple import UndefinedValueError

if __name__ == '__main__':
    try:
        from datos.conexion import base_datos
    except UndefinedValueError:
        print('Falta configurar el archivo .env (copie .env.example y complete sus datos).')
        sys.exit(1)

    from peewee import OperationalError
    from presentacion import menu_principal

    try:
        base_datos.connect()
    except OperationalError:
        print('No se pudo conectar a la base de datos. Revise el archivo .env y que MySQL esté encendido.')
        sys.exit(1)

    try:
        menu_principal()
    except KeyboardInterrupt:  # Ctrl+C: salir sin mostrar un error largo
        print('\nSaliendo del Sistema')
    finally:
        if not base_datos.is_closed():
            base_datos.close()
