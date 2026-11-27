"""Conversiones de formato para mostrar datos en pantalla."""

FORMATO_FECHA = '%d-%m-%Y'
FORMATO_FECHA_HORA = '%d-%m-%Y %H:%M'


def formatear_fecha(fecha):
    """date(2010, 5, 15) -> '15-05-2010'. Si no hay fecha, devuelve '-'."""
    return fecha.strftime(FORMATO_FECHA) if fecha else '-'


def formatear_fecha_hora(fecha_hora):
    """datetime(2026, 11, 27, 9, 30) -> '27-11-2026 09:30'. Si no hay, devuelve '-'."""
    return fecha_hora.strftime(FORMATO_FECHA_HORA) if fecha_hora else '-'


def formatear_monto(monto):
    """45000 -> '$45.000' (separador de miles chileno)."""
    return '$' + f'{int(monto):,}'.replace(',', '.')


def formatear_nota(nota):
    """Decimal('6.5') -> '6.5'. Si no hay nota, devuelve '-'."""
    return '-' if nota is None else f'{nota:.1f}'


def formatear_porcentaje(valor):
    """Decimal('30.00') -> '30%'; 87.5 -> '87.5%'. Si no hay valor, devuelve '-'."""
    if valor is None:
        return '-'
    return f'{float(valor):g}%'


def texto_o_guion(texto):
    """Muestra '-' cuando un campo opcional está vacío."""
    return texto if texto else '-'
