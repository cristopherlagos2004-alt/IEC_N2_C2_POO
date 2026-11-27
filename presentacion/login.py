"""Pantalla de inicio de sesión (login).

Flujo: Aplicación -> Login -> Validación -> Menú Principal.
Si el usuario no se autentica, nunca llega al menú principal.
"""
from auxiliares.constantes import MAX_INTENTOS_LOGIN
from auxiliares.mensajes import (LOGIN_TITULO, LOGIN_BLOQUEADO, LOGIN_INTENTOS_RESTANTES,
                                 LOGIN_SIN_USUARIOS)
from presentacion.consola import mostrar_titulo, pedir_clave


def iniciar_sesion(negocio_usuarios):
    """Pide usuario y contraseña hasta MAX_INTENTOS_LOGIN veces.

    Devuelve True si el login fue correcto, o False si se agotaron los intentos.
    """
    if not negocio_usuarios.hay_usuarios_activos():
        print(LOGIN_SIN_USUARIOS)
        return False

    mostrar_titulo(LOGIN_TITULO)
    for intento in range(1, MAX_INTENTOS_LOGIN + 1):
        nombre_usuario = input('Usuario: ')
        clave = pedir_clave('Contraseña')  # maskpass: se ven asteriscos, no la contraseña
        exito, mensaje = negocio_usuarios.iniciar_sesion(nombre_usuario, clave)
        print(mensaje)
        if exito:
            return True
        restantes = MAX_INTENTOS_LOGIN - intento
        if restantes:
            print(LOGIN_INTENTOS_RESTANTES.format(intentos=restantes))
    print(LOGIN_BLOQUEADO)
    return False
