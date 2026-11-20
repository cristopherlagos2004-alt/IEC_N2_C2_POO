from presentacion.consola import confirmar, pedir_valido
from presentacion.menu_crud import MenuCrud
from presentacion.presentacion_servicios import TEXTO_MONEDA, aviso_cache
from negocio.negocio_servicios import formatear_decimal, formatear_monto


class MenuPagos(MenuCrud):
    def __init__(self, negocio, negocio_apoderados, negocio_servicios):
        super().__init__('Pagos', negocio)
        self.__apoderados = negocio_apoderados
        self.__servicios = negocio_servicios  # Evaluación 3: indicadores económicos

    @property
    def texto_busqueda(self):
        return 'el nombre del apoderado'

    def pedir_datos(self, actual=None):
        estados = ', '.join(self.negocio.estados)
        return {
            'apoderado': self._elegir(self.__apoderados, 'apoderado', 'apoderado', actual),
            'monto': self._pedir('monto', 'Monto en pesos (ej: 45000)', actual),
            'estado': self._pedir('estado', f'Estado ({estados})', actual),
        }

    def opciones_extra(self):
        return [('Registrar pago (marcar como pagado)', self.registrar_pago),
                ('Ver un pago en UF / dólar / euro / UTM', self.ver_en_moneda),
                ('Registrar pago con monto en UF / dólar / euro / UTM',
                 self.registrar_en_moneda)]

    def registrar_pago(self):
        pago = self.seleccionar('marcarlo como pagado')
        if pago is not None:
            _, mensaje = self.negocio.registrar_pago(pago)
            print(mensaje)

    # ----- Evaluación 3: integración con la API de indicadores -----

    def _pedir_servicio(self, campo, texto):
        return pedir_valido(texto, lambda valor: self.__servicios.validar_campo(campo, valor))

    def ver_en_moneda(self):
        """Muestra el monto de un pago guardado convertido a otra moneda."""
        pago = self.seleccionar('ver en otra moneda')
        if pago is None:
            return
        moneda = self._pedir_servicio('moneda', TEXTO_MONEDA)
        indicador, pesos, convertido = self.__servicios.pesos_a_moneda(str(pago.monto), moneda)
        aviso_cache(indicador)
        print(f'Pago {pago.get_id()}: {formatear_monto(pesos)} = '
              f'{formatear_decimal(convertido)} {indicador.nombre}')

    def registrar_en_moneda(self):
        """Ej: mensualidad de 2,5 UF -> se calcula en pesos con la UF de hoy y se guarda."""
        apoderado = self._elegir(self.__apoderados, 'apoderado', 'apoderado')
        moneda = self._pedir_servicio('moneda', TEXTO_MONEDA)
        cantidad = self._pedir_servicio('cantidad', 'Cantidad (ej: 2,5)')
        indicador, cantidad, pesos = self.__servicios.moneda_a_pesos(cantidad, moneda)
        aviso_cache(indicador)
        print(f'{formatear_decimal(cantidad)} {indicador.nombre} = {formatear_monto(pesos)} '
              f'(1 {indicador.nombre} = ${formatear_decimal(indicador.valor)})')
        if not confirmar('¿Registrar el pago por ese monto?'):
            print('Operación cancelada.')
            return
        # Se guarda con el mismo crear() de siempre: pasa por las mismas validaciones
        _, mensaje = self.negocio.crear({'apoderado': apoderado, 'monto': str(pesos),
                                         'estado': 'Pendiente'})
        print(mensaje)
