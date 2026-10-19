from presentacion.menu_crud import MenuCrud


class MenuPeriodos(MenuCrud):
    def __init__(self, negocio):
        super().__init__('Periodos Académicos', negocio)

    @property
    def texto_busqueda(self):
        return 'el año o el estado'

    def pedir_datos(self, actual=None):
        estados = ', '.join(self.negocio.estados)
        return {
            'anio': self._pedir('anio', 'Año', actual),
            'semestre': self._pedir('semestre', 'Semestre (1 o 2)', actual),
            'estado': self._pedir('estado', f'Estado ({estados})', actual),
        }

    def opciones_extra(self):
        return [('Cambiar estado (iniciar / cerrar periodo)', self.cambiar_estado)]

    def cambiar_estado(self):
        periodo = self.seleccionar('cambiar su estado')
        if periodo is None:
            return
        estados = ', '.join(self.negocio.estados)
        nuevo = input(f'Nuevo estado ({estados}): ')
        _, mensaje = self.negocio.cambiar_estado(periodo, nuevo)
        print(mensaje)
