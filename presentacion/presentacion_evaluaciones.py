from presentacion.menu_crud import MenuCrud


class MenuEvaluaciones(MenuCrud):
    def __init__(self, negocio, negocio_asignaturas):
        super().__init__('Evaluaciones', negocio)
        self.__asignaturas = negocio_asignaturas

    def pedir_datos(self, actual=None):
        return {
            'asignatura': self._elegir(self.__asignaturas, 'asignatura', 'asignatura', actual),
            'nombre': self._pedir('nombre', 'Nombre (ej: Prueba 1)', actual),
            'fecha': self._pedir('fecha', 'Fecha (DD-MM-AAAA)', actual),
            'porcentaje': self._pedir('porcentaje', 'Ponderación en % (ej: 30)', actual),
        }
