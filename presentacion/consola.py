"""Funciones de apoyo para leer y mostrar datos en la consola."""
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
