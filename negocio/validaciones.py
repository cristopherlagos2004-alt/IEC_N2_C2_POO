"""Validaciones de datos de entrada. No dependen de la base de datos,
así que se pueden probar solas (ver tests/test_validaciones.py)."""
import re
from datetime import date, datetime

PATRON_RUT = re.compile(r'^\d{7,8}-[\dK]$')


def calcular_dv(numero: str) -> str:
    """Calcula el dígito verificador de un RUT con el algoritmo módulo 11."""
    suma = 0
    multiplicador = 2
    for digito in reversed(numero):
        suma += int(digito) * multiplicador
        multiplicador = 2 if multiplicador == 7 else multiplicador + 1
    resto = 11 - (suma % 11)
    if resto == 11:
        return '0'
    if resto == 10:
        return 'K'
    return str(resto)


def normalizar_rut(rut: str) -> str:
    """Deja el RUT con formato 12345678-9: sin puntos, sin espacios y con K mayúscula."""
    limpio = rut.strip().replace('.', '').replace(' ', '').upper()
    if '-' not in limpio and len(limpio) > 1:
        limpio = f'{limpio[:-1]}-{limpio[-1]}'
    return limpio


def validar_rut(rut: str) -> str:
    """Devuelve el RUT normalizado o lanza ValueError si no es válido."""
    rut = normalizar_rut(rut)
    if not PATRON_RUT.match(rut):
        raise ValueError('El RUT debe tener el formato 12345678-9.')
    numero, dv = rut.split('-')
    if calcular_dv(numero) != dv:
        raise ValueError('El dígito verificador del RUT no es correcto.')
    return rut


def validar_nombre(nombre: str) -> str:
    """Devuelve el nombre limpio y con mayúsculas iniciales, o lanza ValueError."""
    nombre = ' '.join(nombre.split())  # quita espacios dobles y en los extremos
    if not nombre:
        raise ValueError('El nombre no puede estar vacío.')
    if len(nombre) > 100:
        raise ValueError('El nombre no puede tener más de 100 caracteres.')
    if not all(c.isalpha() or c in " '-" for c in nombre):
        raise ValueError('El nombre solo puede tener letras, espacios, guiones o apóstrofes.')
    return nombre.title()


def validar_fecha_nacimiento(texto: str) -> date:
    """Convierte 'YYYY-MM-DD' en fecha, o lanza ValueError."""
    try:
        fecha = datetime.strptime(texto.strip(), '%Y-%m-%d').date()
    except ValueError:
        raise ValueError('La fecha debe tener el formato YYYY-MM-DD (ej: 2010-05-15).')
    if fecha >= date.today():
        raise ValueError('La fecha de nacimiento no puede ser hoy ni una fecha futura.')
    if fecha.year < 1900:
        raise ValueError('La fecha de nacimiento no es realista.')
    return fecha
