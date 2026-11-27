"""Conversiones de formato para mostrar datos en pantalla."""

FORMATO_FECHA = '%d-%m-%Y'


def formatear_fecha(fecha):
    """date(2010, 5, 15) -> '15-05-2010'. Si no hay fecha, devuelve '-'."""
    return fecha.strftime(FORMATO_FECHA) if fecha else '-'


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
