from presentacion.consola import mostrar_tabla
from presentacion.menu_crud import MenuCrud


class MenuAsignaturas(MenuCrud):
    def __init__(self, negocio, negocio_docentes, negocio_cursos):
        super().__init__('Asignaturas', negocio)
        self.__docentes = negocio_docentes
        self.__cursos = negocio_cursos

    @property
    def texto_busqueda(self):
        return 'el nombre o el código'

    def pedir_datos(self, actual=None):
        return {
            'nombre': self._pedir('nombre', 'Nombre', actual),
            'codigo': self._pedir('codigo', 'Código (ej: MAT1)', actual),
            'horasSemanales': self._pedir('horasSemanales', 'Horas semanales', actual),
            'docente': self._elegir(self.__docentes, 'docente', 'docente', actual),
            'curso': self._elegir(self.__cursos, 'curso', 'curso', actual),
        }

    def opciones_extra(self):
        return [('Ver promedio, evaluaciones y estudiantes', self.ver_resumen)]

    def ver_resumen(self):
        asignatura = self.seleccionar('ver su resumen')
        if asignatura is None:
            return
        resumen = self.negocio.resumen(asignatura)
        print(f'\n{asignatura.descripcion()} - Promedio: {resumen["promedio"]}')
        print('\nEvaluaciones:')
        mostrar_tabla(resumen['evaluaciones'])
        print('\nEstudiantes:')
        mostrar_tabla(resumen['estudiantes'])
