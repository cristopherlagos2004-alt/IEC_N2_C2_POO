"""Crea el PRIMER usuario del sistema (Evaluación 3).

Uso:  python3 crear_usuario.py      (en Windows: py crear_usuario.py)

Solo funciona cuando la tabla usuarios está vacía: para entrar al sistema hace
falta un usuario, y para crear usuarios desde el menú hace falta haber entrado.
Los demás usuarios se crean desde el menú "Usuarios", con la sesión iniciada.

La contraseña se escribe dos veces con maskpass (se ven asteriscos) y en la
base de datos solo se guarda su hash bcrypt. Por eso los usuarios no se crean
con un INSERT escrito a mano.
"""
import sys

from datos.conexion import Conexion
from negocio.negocio_autenticacion import Sesion
from negocio.negocio_base import ErrorDatos
from negocio.negocio_usuarios import NegocioUsuarios
from presentacion.consola import OperacionCancelada, pedir_contrasena_nueva, pedir_valido
from presentacion.presentacion_usuarios import REGLAS_CONTRASENA


def main():
    conexion = Conexion()
    exito, mensaje = conexion.conectar()
    if not exito:
        print(mensaje)
        sys.exit(1)

    try:
        # Sesión vacía: NegocioUsuarios solo permite crear_primer_usuario() sin sesión
        negocio = NegocioUsuarios(Sesion())
        print('Crear el primer usuario del sistema\n')
        if negocio.hay_usuarios():
            print('Ya existen usuarios. Inicie sesión con "python3 main.py" y cree los demás '
                  'desde el menú "Usuarios".')
            return
        nombre = pedir_valido('Nombre de usuario', negocio.verificar_nombre_disponible)
        print(REGLAS_CONTRASENA)
        contrasena = pedir_contrasena_nueva(lambda texto: negocio.validar_contrasena(texto, nombre))
        _, mensaje = negocio.crear_primer_usuario({'nombre_usuario': nombre,
                                                   'contrasena': contrasena})
        print(mensaje)
    except (ErrorDatos, OperacionCancelada) as error:
        print(error)
    except (KeyboardInterrupt, EOFError):
        print('\nCancelado.')
    finally:
        conexion.desconectar()


if __name__ == '__main__':
    main()
