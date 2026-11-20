"""Pantalla de inicio de sesión (Evaluación 3)."""
from getpass import getpass

from presentacion.consola import mostrar_titulo

INTENTOS_POR_EJECUCION = 3


def pantalla_login(negocio_autenticacion):
    """Pide usuario y contraseña. Devuelve True si se inició sesión.

    - getpass() no muestra la contraseña mientras se escribe.
    - Después de 3 intentos fallidos el programa se cierra (además, la base de
      datos bloquea la cuenta unos minutos; ver NegocioAutenticacion).
    """
    mostrar_titulo('Inicio de sesión')
    for intento in range(1, INTENTOS_POR_EJECUCION + 1):
        usuario = input('Usuario: ')
        contrasena = getpass('Contraseña: ')
        exito, mensaje = negocio_autenticacion.iniciar_sesion(usuario, contrasena)
        print(mensaje)
        if exito:
            return True
        restantes = INTENTOS_POR_EJECUCION - intento
        if restantes:
            print(f'Le quedan {restantes} intento(s).\n')
    print('Demasiados intentos fallidos.')
    return False
