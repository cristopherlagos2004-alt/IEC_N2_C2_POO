"""Punto de inicio del Sistema de Gestión Escolar.

Flujo: Aplicación -> Login -> Validación -> Menú Principal.
No se puede llegar al menú principal sin iniciar sesión.
"""
import sys

from auxiliares.mensajes import SALIENDO
from datos.conexion import Conexion
from negocio.negocio_base import ErrorDatos
from negocio.negocio_usuarios import NegocioUsuarios
from presentacion import MenuPrincipal
from presentacion.login import iniciar_sesion


def main():
    conexion = Conexion()
    exito, mensaje = conexion.conectar()
    if not exito:
        print(mensaje)
        sys.exit(1)

    try:
        negocio_usuarios = NegocioUsuarios()
        if iniciar_sesion(negocio_usuarios):          # Login + validación
            MenuPrincipal(negocio_usuarios).mostrar()  # Menú principal (solo si entró)
        else:
            sys.exit(1)
    except ErrorDatos as error:  # ej: falta crear la tabla usuarios
        print(error)
        sys.exit(1)
    except (KeyboardInterrupt, EOFError):  # Ctrl+C: salir sin mostrar un error largo
        print(f'\n{SALIENDO}')
    finally:
        conexion.desconectar()


if __name__ == '__main__':
    main()
