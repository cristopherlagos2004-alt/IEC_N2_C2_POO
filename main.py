"""Punto de inicio del Sistema de Gestión Escolar."""
import sys

from datos.conexion import Conexion
from negocio.negocio_autenticacion import NegocioAutenticacion, Sesion
from presentacion import MenuPrincipal
from presentacion.consola import OperacionCancelada
from presentacion.presentacion_login import pantalla_login


def main():
    conexion = Conexion()
    exito, mensaje = conexion.conectar()
    if not exito:
        print(mensaje)
        sys.exit(1)

    sesion = Sesion()
    try:
        # Evaluación 3: sin iniciar sesión no se llega al menú (ni a las APIs)
        if not pantalla_login(NegocioAutenticacion(sesion)):
            sys.exit(1)
        MenuPrincipal(sesion).mostrar()
    except OperacionCancelada as error:  # ej: se ejecutó sin terminal y no se puede pedir la contraseña
        print(error)
        sys.exit(1)
    except (KeyboardInterrupt, EOFError):  # Ctrl+C: salir sin mostrar un error largo
        print('\nSaliendo del Sistema')
    finally:
        sesion.cerrar()
        conexion.desconectar()


if __name__ == '__main__':
    main()
