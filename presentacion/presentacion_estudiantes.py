from presentacion.consola import mostrar_tabla
from presentacion.menu_crud import MenuCrud


class MenuEstudiantes(MenuCrud):
    def __init__(self, negocio, negocio_cursos, negocio_apoderados):
        super().__init__('Estudiantes', negocio)
        self.__cursos = negocio_cursos
        self.__apoderados = negocio_apoderados

    def pedir_datos(self, actual=None):
        return {
            'rut': self._pedir('rut', 'RUT (ej: 12345678-9)', actual),
            'nombre': self._pedir('nombre', 'Nombre', actual),
            'fecha_nacimiento': self._pedir('fecha_nacimiento', 'Fecha de nacimiento (DD-MM-AAAA)',
                                            actual),
            'curso': self._elegir(self.__cursos, 'curso', 'curso', actual),
            'apoderado': self._elegir(self.__apoderados, 'apoderado', 'apoderado', actual),
        }

    def opciones_extra(self):
        return [('Ver ficha académica (promedio, asistencia y notas)', self.ver_ficha)]

    def ver_ficha(self):
        estudiante = self.seleccionar('ver su ficha')
        if estudiante is None:
            return
        ficha = self.negocio.ficha(estudiante)
        print()
        print(ficha['datos'])
        print(f'Promedio general: {ficha["promedio"]}')
        print(f'Asistencia: {ficha["asistencia"]}')
        print('\nNotas:')
        mostrar_tabla(ficha['notas'])
        print('\nAsignaturas de su curso:')
        mostrar_tabla(ficha['asignaturas'])
