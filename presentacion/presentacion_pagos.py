from presentacion.menu_crud import MenuCrud


class MenuPagos(MenuCrud):
    def __init__(self, negocio, negocio_apoderados):
        super().__init__('Pagos', negocio)
        self.__apoderados = negocio_apoderados

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
        return [('Registrar pago (marcar como pagado)', self.registrar_pago)]

    def registrar_pago(self):
        pago = self.seleccionar('marcarlo como pagado')
        if pago is not None:
            _, mensaje = self.negocio.registrar_pago(pago)
            print(mensaje)
