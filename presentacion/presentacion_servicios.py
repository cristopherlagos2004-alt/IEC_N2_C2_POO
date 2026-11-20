"""Menú de servicios externos: indicadores económicos y clima (Evaluación 3)."""
from negocio.negocio_servicios import formatear_decimal, formatear_fecha, formatear_monto
from presentacion.consola import pedir_valido
from presentacion.menu_base import MenuBase

TEXTO_MONEDA = 'Moneda (UF, dólar, euro o UTM)'


def mostrar_indicador(indicador):
    texto = (f'{indicador.nombre:<6} ${formatear_decimal(indicador.valor)} '
             f'(valor del {formatear_fecha(indicador.fecha)})')
    if indicador.desde_cache:
        texto += '  [sin conexión: último valor guardado]'
    print(texto)


def aviso_cache(indicador):
    if indicador.desde_cache:
        print(f'Aviso: no se pudo consultar la API. Se usó el último valor guardado '
              f'({formatear_fecha(indicador.fecha)}).')


class MenuServiciosExternos(MenuBase):
    """Herencia: usa la forma de mostrar menús de MenuBase.
    Solo pide datos y muestra resultados; las reglas y el control de sesión
    están en NegocioServiciosExternos."""

    def __init__(self, negocio):
        super().__init__('Servicios externos (indicadores y clima)')
        self.__negocio = negocio

    def opciones(self):
        return [
            ('Indicadores económicos del día', self.indicadores_del_dia),
            ('Convertir pesos a UF / dólar / euro / UTM', self.pesos_a_moneda),
            ('Convertir UF / dólar / euro / UTM a pesos', self.moneda_a_pesos),
            ('Clima para una actividad al aire libre', self.clima_para_actividad),
        ]

    def _pedir(self, campo, texto):
        return pedir_valido(texto, lambda valor: self.__negocio.validar_campo(campo, valor))

    def indicadores_del_dia(self):
        print('Consultando mindicador.cl...')
        indicadores, errores = self.__negocio.indicadores_del_dia()
        for indicador in indicadores:
            mostrar_indicador(indicador)
        for error in errores:
            print(f'  >> {error}')

    def pesos_a_moneda(self):
        monto = self._pedir('monto', 'Monto en pesos (ej: 45000)')
        moneda = self._pedir('moneda', TEXTO_MONEDA)
        indicador, pesos, convertido = self.__negocio.pesos_a_moneda(monto, moneda)
        aviso_cache(indicador)
        print(f'{formatear_monto(pesos)} = {formatear_decimal(convertido)} {indicador.nombre} '
              f'(1 {indicador.nombre} = ${formatear_decimal(indicador.valor)})')

    def moneda_a_pesos(self):
        moneda = self._pedir('moneda', TEXTO_MONEDA)
        cantidad = self._pedir('cantidad', 'Cantidad (ej: 2,5)')
        indicador, cantidad, pesos = self.__negocio.moneda_a_pesos(cantidad, moneda)
        aviso_cache(indicador)
        print(f'{formatear_decimal(cantidad)} {indicador.nombre} = {formatear_monto(pesos)}')

    def clima_para_actividad(self):
        ciudad = self._pedir('ciudad', 'Ciudad (ej: Temuco)')
        pais = self._pedir('pais', 'Código de país (ENTER = CL)')
        print('Consultando OpenWeatherMap...')
        clima, recomendacion, _ = self.__negocio.clima_para_actividad(ciudad, pais)
        print(f'\nClima en {clima.ciudad} ({clima.pais}): {clima.descripcion}')
        print(f'Temperatura: {clima.temperatura:.1f} °C (sensación {clima.sensacion:.1f} °C)')
        print(f'Humedad: {clima.humedad}%   Viento: {clima.viento:.1f} m/s')
        print(f'\n{recomendacion}')
