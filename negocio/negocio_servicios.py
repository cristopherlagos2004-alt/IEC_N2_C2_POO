"""Reglas de negocio que usan servicios externos (Evaluación 3).

- Indicadores económicos: convertir montos de pagos entre pesos y UF / dólar / euro / UTM.
- Clima: recomendar si conviene hacer una actividad al aire libre (educación física,
  salida pedagógica).

Control de acceso: TODOS los métodos públicos llaman primero a sesion.exigir().
La presentación solo puede llegar a las APIs a través de esta clase, así que sin
sesión iniciada no hay forma de consumirlas.
"""
from decimal import Decimal, ROUND_HALF_UP

from datos.auxiliares.validaciones import (validar_monto, validar_moneda, validar_decimal,
                                           validar_ciudad, validar_codigo_pais)
from datos.auxiliares.errores import ErrorDatos
from datos.servicios.errores_servicio import ErrorServicioExterno
# La presentación recibe los formatos a través de negocio (no importa la capa de datos)
from datos.auxiliares.formatos import formatear_decimal, formatear_fecha, formatear_monto  # noqa: F401
from datos.servicios.servicio_clima import ServicioClima
from datos.servicios.servicio_indicadores import ServicioIndicadores

MONEDAS_DEL_DIA = ('uf', 'dolar', 'euro', 'utm')


def validar_cantidad(texto):
    """Cantidad en UF, dólares, etc.: de 0,01 a 100.000, con hasta 2 decimales."""
    return validar_decimal(texto, 'La cantidad', Decimal('0.01'), Decimal('100000'), 2)


class NegocioServiciosExternos:
    """Encapsulamiento: la sesión y los servicios son atributos privados."""

    # La presentación usa esto para avisar al tiro si un dato está mal (igual que NegocioBase)
    validadores = {
        'monto': validar_monto,
        'moneda': validar_moneda,
        'cantidad': validar_cantidad,
        'ciudad': validar_ciudad,
        'pais': validar_codigo_pais,
    }

    def __init__(self, sesion, servicio_indicadores=None, servicio_clima=None):
        self.__sesion = sesion
        self.__indicadores = servicio_indicadores or ServicioIndicadores()
        self.__clima = servicio_clima or ServicioClima()

    def validar_campo(self, campo, texto):
        """Lanza ValueError si el dato está mal (la presentación lo usa para volver a pedirlo)."""
        return self.validadores[campo](texto)

    def _validar(self, campo, texto):
        """Igual que validar_campo, pero lanza ErrorDatos: el menú muestra el mensaje
        sin tratarlo como un error inesperado. Se vuelve a validar aquí aunque la
        presentación ya lo haya hecho (defensa en profundidad)."""
        try:
            return self.validar_campo(campo, texto)
        except ValueError as error:
            raise ErrorDatos(str(error)) from None

    # ----- Indicadores económicos -----

    def indicadores_del_dia(self):
        """Devuelve (lista de Indicador, lista de mensajes de error).

        Si falla un indicador, los demás se muestran igual (continuidad).
        """
        self.__sesion.exigir()
        indicadores, errores = [], []
        for codigo in MONEDAS_DEL_DIA:
            try:
                indicadores.append(self.__indicadores.obtener(codigo))
            except ErrorServicioExterno as error:
                errores.append(f'{codigo.upper()}: {error}')
        return indicadores, errores

    def pesos_a_moneda(self, monto_texto, moneda_texto):
        """'45000', 'dolar' -> (Indicador, monto en pesos, Decimal en dólares)."""
        self.__sesion.exigir()
        monto = self._validar('monto', monto_texto)
        indicador = self.__indicadores.obtener(self._validar('moneda', moneda_texto))
        convertido = (Decimal(monto) / indicador.valor).quantize(Decimal('0.01'), ROUND_HALF_UP)
        return indicador, monto, convertido

    def moneda_a_pesos(self, cantidad_texto, moneda_texto):
        """'2,5', 'uf' -> (Indicador, cantidad, pesos enteros). Para cobrar en UF, por ejemplo."""
        self.__sesion.exigir()
        cantidad = self._validar('cantidad', cantidad_texto)
        indicador = self.__indicadores.obtener(self._validar('moneda', moneda_texto))
        pesos = int((cantidad * indicador.valor).quantize(Decimal('1'), ROUND_HALF_UP))
        if pesos < 1:
            raise ErrorDatos('El monto en pesos resultó menor que $1.')
        return indicador, cantidad, pesos

    # ----- Clima -----

    def clima_para_actividad(self, ciudad_texto, pais_texto=''):
        """Devuelve (Clima, recomendacion, apta). apta: True / False."""
        self.__sesion.exigir()
        ciudad = self._validar('ciudad', ciudad_texto)
        pais = self._validar('pais', pais_texto)
        clima = self.__clima.obtener(ciudad, pais)
        apta, recomendacion = evaluar_actividad(clima)
        return clima, recomendacion, apta


def evaluar_actividad(clima):
    """Regla de negocio: ¿conviene hacer una actividad al aire libre con este clima?

    Devuelve (apta, motivo). Usa el código de condición de OpenWeatherMap
    (no el texto), porque el texto cambia según el idioma.
    """
    grupo = clima.codigo_condicion // 100
    if grupo == 2:
        return False, 'No recomendable: hay tormenta eléctrica.'
    if grupo in (3, 5):
        return False, 'No recomendable: hay lluvia o llovizna. Prefiera el gimnasio.'
    if grupo == 6:
        return False, 'No recomendable: hay nieve.'
    if clima.temperatura >= 32:
        return False, 'No recomendable: hace demasiado calor (riesgo de golpe de calor).'
    if clima.temperatura <= 3:
        return False, 'No recomendable: hace demasiado frío.'
    if clima.viento >= 12:
        return False, 'No recomendable: hay viento muy fuerte.'
    avisos = []
    if grupo == 7:
        avisos.append('hay niebla o poca visibilidad')
    if clima.temperatura >= 27:
        avisos.append('hace calor: lleven agua y bloqueador')
    if clima.temperatura <= 8:
        avisos.append('hace frío: lleven abrigo')
    if avisos:
        return True, 'Recomendable con precaución: ' + '; '.join(avisos) + '.'
    return True, 'Recomendable: el clima es adecuado para actividades al aire libre.'
