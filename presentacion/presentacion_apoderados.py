from presentacion.menu_crud import MenuCrud


class MenuApoderados(MenuCrud):
    def __init__(self, negocio):
        super().__init__('Apoderados', negocio)

    def pedir_datos(self, actual=None):
        return {
            'rut': self._pedir('rut', 'RUT (ej: 12345678-9)', actual),
            'nombre': self._pedir('nombre', 'Nombre', actual),
            'telefono': self._pedir('telefono', 'Teléfono (opcional, ej: +56912345678)', actual),
        }

    def opciones_extra(self):
        return [('Ver ficha del apoderado', self.ver_ficha)]

    def ver_ficha(self):
        apoderado = self.seleccionar('ver su ficha')
        if apoderado is not None:
            print()
            print(self.negocio.ficha(apoderado))
