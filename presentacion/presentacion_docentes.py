from presentacion.consola import mostrar_tabla
from presentacion.menu_crud import MenuCrud


class MenuDocentes(MenuCrud):
    def __init__(self, negocio):
        super().__init__('Docentes', negocio)

    def pedir_datos(self, actual=None):
        return {
            'nombre': self._pedir('nombre', 'Nombre', actual),
            'correo': self._pedir('correo', 'Correo (opcional)', actual),
            'especialidad': self._pedir('especialidad', 'Especialidad (opcional)', actual),
        }

    def opciones_extra(self):
        return [('Ver asignaturas y estudiantes del docente', self.ver_ficha)]

    def ver_ficha(self):
        docente = self.seleccionar('ver su ficha')
        if docente is None:
            return
        ficha = self.negocio.ficha(docente)
        print()
        print(ficha['datos'])
        print('\nAsignaturas que imparte:')
        mostrar_tabla(ficha['asignaturas'])
        print('\nSus estudiantes:')
        mostrar_tabla(ficha['estudiantes'])
