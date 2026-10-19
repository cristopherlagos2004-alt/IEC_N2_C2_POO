"""Validaciones de datos de entrada.

Todas reciben texto (lo que escribió el usuario) y devuelven el valor limpio
y convertido, o lanzan ValueError con un mensaje para el usuario.
No dependen de la base de datos, así que se pueden probar solas
(ver tests/test_validaciones.py).
"""
import re
from datetime import date, datetime
from decimal import Decimal, InvalidOperation

PATRON_RUT = re.compile(r'^\d{7,8}-[\dK]$')
PATRON_CORREO = re.compile(r'^[\w.+-]+@[\w-]+(\.[\w-]+)+$')
PATRON_TELEFONO = re.compile(r'^\+?\d{8,15}$')
FORMATOS_FECHA = ('%d-%m-%Y', '%d/%m/%Y', '%Y-%m-%d')


def _limpiar(texto):
    return '' if texto is None else str(texto).strip()


# ---------- RUT ----------

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


def normalizar_rut(rut) -> str:
    """Deja el RUT con formato 12345678-9: sin puntos, sin espacios y con K mayúscula."""
    limpio = _limpiar(rut).replace('.', '').replace(' ', '').upper()
    if '-' not in limpio and len(limpio) > 1:
        limpio = f'{limpio[:-1]}-{limpio[-1]}'
    return limpio


def validar_rut(rut) -> str:
    """Devuelve el RUT normalizado o lanza ValueError si no es válido."""
    rut = normalizar_rut(rut)
    if not PATRON_RUT.match(rut):
        raise ValueError('El RUT debe tener el formato 12345678-9.')
    numero, dv = rut.split('-')
    if calcular_dv(numero) != dv:
        raise ValueError('El dígito verificador del RUT no es correcto.')
    return rut


# ---------- Textos ----------

def validar_nombre(nombre, campo='El nombre') -> str:
    """Nombre de persona: solo letras, espacios, guiones o apóstrofes."""
    nombre = ' '.join(_limpiar(nombre).split())  # quita espacios dobles
    if not nombre:
        raise ValueError(f'{campo} no puede estar vacío.')
    if len(nombre) > 100:
        raise ValueError(f'{campo} no puede tener más de 100 caracteres.')
    if not all(c.isalpha() or c in " '-" for c in nombre):
        raise ValueError(f'{campo} solo puede tener letras, espacios, guiones o apóstrofes.')
    return nombre.title()


def validar_texto(texto, campo, max_largo, obligatorio=True):
    """Texto libre. Si es opcional y viene vacío, devuelve None."""
    texto = ' '.join(_limpiar(texto).split())
    if not texto:
        if obligatorio:
            raise ValueError(f'{campo} no puede estar vacío.')
        return None
    if len(texto) > max_largo:
        raise ValueError(f'{campo} no puede tener más de {max_largo} caracteres.')
    return texto


def validar_codigo(codigo, campo='El código', max_largo=20):
    """Código en mayúsculas y sin espacios ('mat 1' -> 'MAT1'): letras, números o guiones."""
    codigo = _limpiar(codigo).upper().replace(' ', '')
    if not codigo:
        raise ValueError(f'{campo} no puede estar vacío.')
    if len(codigo) > max_largo:
        raise ValueError(f'{campo} no puede tener más de {max_largo} caracteres.')
    if not all(c.isalnum() or c == '-' for c in codigo):
        raise ValueError(f'{campo} solo puede tener letras, números o guiones.')
    return codigo


def validar_correo(correo):
    """Correo opcional. Vacío -> None."""
    correo = _limpiar(correo).lower()
    if not correo:
        return None
    if len(correo) > 100 or not PATRON_CORREO.match(correo):
        raise ValueError('El correo no es válido (ej: nombre@colegio.cl).')
    return correo


def validar_telefono(telefono):
    """Teléfono opcional, solo dígitos (puede empezar con +). Vacío -> None."""
    telefono = _limpiar(telefono).replace(' ', '').replace('-', '')
    if not telefono:
        return None
    if not PATRON_TELEFONO.match(telefono):
        raise ValueError('El teléfono debe tener entre 8 y 15 dígitos (ej: +56912345678).')
    return telefono


def validar_opcion(texto, campo, opciones):
    """El texto debe ser una de las opciones (sin importar mayúsculas)."""
    texto = _limpiar(texto)
    for opcion in opciones:
        if texto.lower() == opcion.lower():
            return opcion
    raise ValueError(f'{campo} debe ser una de estas opciones: {", ".join(opciones)}.')


def validar_si_no(texto, campo) -> bool:
    texto = _limpiar(texto).lower()
    if texto in ('s', 'si', 'sí', 'true', '1'):
        return True
    if texto in ('n', 'no', 'false', '0'):
        return False
    raise ValueError(f'{campo}: responda s (sí) o n (no).')


# ---------- Números ----------

def validar_entero(texto, campo, minimo=None, maximo=None) -> int:
    texto = _limpiar(texto)
    try:
        valor = int(texto)
    except ValueError:
        raise ValueError(f'{campo} debe ser un número entero.')
    if minimo is not None and valor < minimo:
        raise ValueError(f'{campo} debe ser mayor o igual a {minimo}.')
    if maximo is not None and valor > maximo:
        raise ValueError(f'{campo} debe ser menor o igual a {maximo}.')
    return valor


def validar_decimal(texto, campo, minimo, maximo, decimales) -> Decimal:
    """Número con decimales; acepta coma o punto (6,5 o 6.5)."""
    texto = _limpiar(texto).replace(',', '.')
    try:
        valor = Decimal(texto)
    except InvalidOperation:
        raise ValueError(f'{campo} debe ser un número.')
    if not valor.is_finite():
        raise ValueError(f'{campo} debe ser un número.')
    # normalize() quita ceros sobrantes: 6.50 -> 6.5, así 6.50 cuenta como 1 decimal
    if valor.normalize().as_tuple().exponent < -decimales:
        raise ValueError(f'{campo} puede tener como máximo {decimales} decimal(es).')
    if not minimo <= valor <= maximo:
        raise ValueError(f'{campo} debe estar entre {minimo} y {maximo}.')
    return valor.quantize(Decimal(1).scaleb(-decimales))  # 6.5 -> 6.5 ; 30 -> 30.00


def validar_nota(texto) -> Decimal:
    """Nota chilena: de 1.0 a 7.0, con un decimal."""
    return validar_decimal(texto, 'La nota', Decimal('1.0'), Decimal('7.0'), 1)


def validar_porcentaje(texto) -> Decimal:
    """Ponderación de una evaluación: mayor que 0 y hasta 100."""
    valor = validar_decimal(texto, 'El porcentaje', Decimal('0'), Decimal('100'), 2)
    if valor == 0:
        raise ValueError('El porcentaje debe ser mayor que 0.')
    return valor


def validar_monto(texto) -> int:
    """Monto en pesos chilenos. Acepta '$45.000' o '45000'."""
    texto = _limpiar(texto).replace('$', '').replace('.', '').replace(' ', '')
    return validar_entero(texto, 'El monto', minimo=1)


# ---------- Fechas ----------

def validar_fecha(texto, campo='La fecha') -> date:
    """Acepta DD-MM-AAAA, DD/MM/AAAA o AAAA-MM-DD."""
    texto = _limpiar(texto)
    for formato in FORMATOS_FECHA:
        try:
            return datetime.strptime(texto, formato).date()
        except ValueError:
            continue
    raise ValueError(f'{campo} debe tener el formato DD-MM-AAAA (ej: 15-05-2010).')


def validar_fecha_nacimiento(texto) -> date:
    fecha = validar_fecha(texto, 'La fecha de nacimiento')
    if fecha >= date.today():
        raise ValueError('La fecha de nacimiento no puede ser hoy ni una fecha futura.')
    if fecha.year < 1900:
        raise ValueError('La fecha de nacimiento no es realista.')
    return fecha


def validar_fecha_o_hoy(texto, campo='La fecha') -> date:
    """Si viene vacía, usa la fecha de hoy."""
    return date.today() if not _limpiar(texto) else validar_fecha(texto, campo)


def validar_fecha_hasta_hoy(texto, campo='La fecha') -> date:
    """Fecha de algo que ya pasó (asistencia, registro de nota). Vacía = hoy."""
    fecha = validar_fecha_o_hoy(texto, campo)
    if fecha > date.today():
        raise ValueError(f'{campo} no puede ser una fecha futura.')
    return fecha
