from presentacion.menu_crud import MenuCrud


class MenuAsistencias(MenuCrud):
    def __init__(self, negocio, negocio_estudiantes):
        super().__init__('Asistencias', negocio)
        self.__estudiantes = negocio_estudiantes

    @property
    def texto_busqueda(self):
        return 'el nombre del estudiante'

    def pedir_datos(self, actual=None):
        return {
            'estudiante': self._elegir(self.__estudiantes, 'estudiante', 'estudiante', actual),
            'fecha': self._pedir('fecha', 'Fecha (DD-MM-AAAA, ENTER = hoy)', actual),
            'presente': self._pedir('presente', '¿Presente? (s/n)', actual),
            'observacion': self._pedir('observacion', 'Observación (opcional)', actual),
        }
