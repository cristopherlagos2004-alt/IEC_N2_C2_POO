"""Crea un usuario para iniciar sesión en el sistema (Evaluación 3).

Uso:  python3 crear_usuario.py      (en Windows: py crear_usuario.py)

La contraseña se escribe dos veces, sin que se vea en pantalla, y en la base
de datos solo se guarda su hash. Por eso los usuarios se crean con este script
y no con un INSERT escrito a mano.
"""
import sys
from getpass import getpass

from datos.conexion import Conexion
from datos.auxiliares.errores import ErrorDatos
from negocio.negocio_autenticacion import NegocioAutenticacion, Sesion


def main():
    conexion = Conexion()
    exito, mensaje = conexion.conectar()
    if not exito:
        print(mensaje)
        sys.exit(1)

    try:
        print('Crear usuario del sistema')
        print('La contraseña debe tener al menos 8 caracteres, con letras y números.\n')
        nombre = input('Nombre de usuario: ')
        contrasena = getpass('Contraseña: ')
        if contrasena != getpass('Repita la contraseña: '):
            print('Las contraseñas no coinciden.')
            sys.exit(1)
        _, mensaje = NegocioAutenticacion(Sesion()).crear_usuario(nombre, contrasena)
        print(mensaje)
    except ErrorDatos as error:
        print(error)
    except (KeyboardInterrupt, EOFError):
        print('\nCancelado.')
    finally:
        conexion.desconectar()


if __name__ == '__main__':
    main()
