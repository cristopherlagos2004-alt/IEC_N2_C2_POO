"""Funciones de apoyo para leer y mostrar datos en la consola."""
import sys

import maskpass
from prettytable import PrettyTable

# Marca que indica "registro nuevo": no hay un valor actual que conservar.
SIN_VALOR = object()


class OperacionCancelada(Exception):
    """Se lanza cuando una operación no puede continuar (ej: no hay cursos para elegir).
    El menú la captura y muestra el mensaje, sin cerrar el programa."""


def mostrar_titulo(titulo):
    print()
    print(titulo)
    print('=' * len(titulo))


def mostrar_tabla(registros):
    """Muestra cualquier lista de registros en una tabla.

    Polimorfismo: sirve para todos los modelos, porque cada uno define
    a su manera columnas() y fila().
    """
    if not registros:
        print('No hay registros para mostrar.')
        return
    tabla = PrettyTable()
    tabla.field_names = registros[0].columnas()
    for registro in registros:
        tabla.add_row(registro.fila())
    print(tabla)


def pedir(texto, actual=SIN_VALOR):
    """Pide un dato al usuario.

    - Registro nuevo (actual = SIN_VALOR): devuelve lo que escriba.
    - Actualización: muestra el valor actual entre [ ].
      ENTER conserva ese valor y "-" deja el campo vacío.
    """
    if actual is SIN_VALOR:
        return input(f'{texto}: ').strip()
    mostrado = '-' if actual in (None, '') else actual
    valor = input(f'{texto} [{mostrado}]: ').strip()
    if valor == '-':
        return ''
    if valor == '':
        return '' if actual is None else str(actual)
    return valor


def confirmar(pregunta):
    return input(f'{pregunta} (s/n): ').strip().lower() in ('s', 'si', 'sí')


def pedir_contrasena(texto='Contraseña'):
    """Pide una contraseña mostrando un * por cada carácter (maskpass, Evaluación 3).

    Es el ÚNICO lugar del programa donde se lee una contraseña: el login, el
    menú Usuarios y crear_usuario.py llaman a esta función.
    - maskpass.askpass() lee tecla por tecla, así la contraseña no queda en pantalla.
    - ESC borra lo escrito (devuelve ''), y Ctrl+C lanza KeyboardInterrupt.
    - Si se borra con retroceso una ñ o una letra con tilde, maskpass puede dejar
      la mitad de esa letra y falla al leerla (UnicodeDecodeError): se vuelve a pedir.
    """
    if not sys.stdin.isatty():
        # maskpass necesita una terminal real (no funciona con la entrada redirigida)
        raise OperacionCancelada('Para escribir la contraseña ejecute el programa desde una terminal.')
    while True:
        try:
            return maskpass.askpass(prompt=f'{texto}: ', mask='*')
        except UnicodeDecodeError:
            print('  >> No se pudo leer la contraseña. Escríbala de nuevo.')


def pedir_contrasena_nueva(validar):
    """Pide una contraseña nueva dos veces, hasta que sea válida y ambas coincidan.

    validar: función de la capa de negocio que lanza ValueError si no sirve.
    Devuelve la contraseña (en texto) para que negocio calcule el hash.
    """
    while True:
        contrasena = pedir_contrasena('Contraseña nueva')
        try:
            validar(contrasena)
        except ValueError as error:
            print(f'  >> {error} Intente nuevamente.')
            continue
        if contrasena == pedir_contrasena('Repita la contraseña'):
            return contrasena
        print('  >> Las contraseñas no coinciden. Intente nuevamente.')


def pedir_valido(texto, validar):
    """Pide un dato hasta que la función validar() lo acepte (no lanza ValueError).

    ENTER sin escribir nada en un dato obligatorio también muestra el motivo.
    Escribir 'c' cancela la operación.
    """
    while True:
        valor = input(f'{texto} (c = cancelar): ').strip()
        if valor.lower() == 'c':
            raise OperacionCancelada('Operación cancelada.')
        try:
            validar(valor)
            return valor
        except ValueError as error:
            print(f'  >> {error} Intente nuevamente.')
