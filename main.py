"""Punto de inicio del Sistema de Gestión Escolar."""
import sys

from datos.conexion import Conexion
from presentacion import MenuPrincipal


def main():
    conexion = Conexion()
    exito, mensaje = conexion.conectar()
    if not exito:
        print(mensaje)
        sys.exit(1)

    try:
        MenuPrincipal().mostrar()
    except (KeyboardInterrupt, EOFError):  # Ctrl+C: salir sin mostrar un error largo
        print('\nSaliendo del Sistema')
    finally:
        conexion.desconectar()


if __name__ == '__main__':
    main()
