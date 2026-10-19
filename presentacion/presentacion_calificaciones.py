from presentacion.menu_crud import MenuCrud


class MenuCalificaciones(MenuCrud):
    def __init__(self, negocio, negocio_estudiantes, negocio_evaluaciones):
        super().__init__('Calificaciones', negocio)
        self.__estudiantes = negocio_estudiantes
        self.__evaluaciones = negocio_evaluaciones

    @property
    def texto_busqueda(self):
        return 'el nombre del estudiante'

    def pedir_datos(self, actual=None):
        return {
            'evaluacion': self._elegir(self.__evaluaciones, 'evaluación', 'evaluacion', actual),
            'estudiante': self._elegir(self.__estudiantes, 'estudiante', 'estudiante', actual),
            'nota': self._pedir('nota', 'Nota (1.0 a 7.0)', actual),
            'fechaRegistro': self._pedir('fechaRegistro',
                                         'Fecha de registro (DD-MM-AAAA, ENTER = hoy)', actual),
            'observacion': self._pedir('observacion', 'Observación (opcional)', actual),
        }
