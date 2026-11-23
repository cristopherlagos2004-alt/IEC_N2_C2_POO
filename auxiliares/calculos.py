"""Utilidades matemáticas que usan varios modelos."""
from decimal import Decimal, ROUND_HALF_UP


def promedio_notas(notas):
    """Promedio con un decimal, redondeando como en Chile (6.45 -> 6.5).
    Si no hay notas, devuelve None."""
    notas = [Decimal(str(nota)) for nota in notas]
    if not notas:
        return None
    promedio = sum(notas) / len(notas)
    return promedio.quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)


def porcentaje(parte, total):
    """Porcentaje con un decimal (3 de 4 -> 75.0). Si total es 0, devuelve None."""
    if total == 0:
        return None
    return round(parte * 100 / total, 1)
