from presentacion.consola import mostrar_tabla
from presentacion.menu_crud import MenuCrud


class MenuCursos(MenuCrud):
    def __init__(self, negocio, negocio_periodos):
        super().__init__('Cursos', negocio)
        self.__periodos = negocio_periodos

    def pedir_datos(self, actual=None):
        jornadas = ', '.join(self.negocio.jornadas)
        return {
            'nombre': self._pedir('nombre', 'Nombre (ej: 1° Medio A)', actual),
            'nivel': self._pedir('nivel', 'Nivel (1 a 12)', actual),
            'jornada': self._pedir('jornada', f'Jornada ({jornadas})', actual),
            'periodo': self._elegir(self.__periodos, 'periodo académico', 'periodo', actual),
        }

    def opciones_extra(self):
        return [('Ver estudiantes del curso', self.ver_estudiantes)]

    def ver_estudiantes(self):
        curso = self.seleccionar('ver sus estudiantes')
        if curso is not None:
            print(f'\nEstudiantes de {curso.nombre}:')
            mostrar_tabla(self.negocio.estudiantes_del_curso(curso))
