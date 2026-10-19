from negocio.negocio_periodos import NegocioPeriodos
from negocio.negocio_cursos import NegocioCursos
from negocio.negocio_docentes import NegocioDocentes
from negocio.negocio_asignaturas import NegocioAsignaturas
from negocio.negocio_apoderados import NegocioApoderados
from negocio.negocio_estudiantes import NegocioEstudiantes
from negocio.negocio_evaluaciones import NegocioEvaluaciones
from negocio.negocio_calificaciones import NegocioCalificaciones
from negocio.negocio_asistencias import NegocioAsistencias
from negocio.negocio_pagos import NegocioPagos
from presentacion.menu_autor import solicitar_datos_autor
from presentacion.menu_base import MenuBase
from presentacion.presentacion_periodos import MenuPeriodos
from presentacion.presentacion_cursos import MenuCursos
from presentacion.presentacion_docentes import MenuDocentes
from presentacion.presentacion_asignaturas import MenuAsignaturas
from presentacion.presentacion_apoderados import MenuApoderados
from presentacion.presentacion_estudiantes import MenuEstudiantes
from presentacion.presentacion_evaluaciones import MenuEvaluaciones
from presentacion.presentacion_calificaciones import MenuCalificaciones
from presentacion.presentacion_asistencias import MenuAsistencias
from presentacion.presentacion_pagos import MenuPagos

NOMBRE_APP = 'Sistema de Gestión Escolar - INACAP'
VERSION_APP = 'v2.0'


class MenuPrincipal(MenuBase):
    """Menú principal: permite navegar por todos los componentes del sistema.

    Polimorfismo: guarda una lista de submenús de distintas clases y a todos
    los trata igual (llama a su método mostrar()); cada uno responde a su manera.
    """

    def __init__(self):
        super().__init__(f'{NOMBRE_APP} {VERSION_APP}', texto_salida='Salir')

        # Una sola instancia de cada clase de negocio, compartida entre los menús
        periodos = NegocioPeriodos()
        cursos = NegocioCursos()
        docentes = NegocioDocentes()
        asignaturas = NegocioAsignaturas()
        apoderados = NegocioApoderados()
        estudiantes = NegocioEstudiantes()
        evaluaciones = NegocioEvaluaciones()

        self.__submenus = [
            MenuEstudiantes(estudiantes, cursos, apoderados),
            MenuCursos(cursos, periodos),
            MenuDocentes(docentes),
            MenuAsignaturas(asignaturas, docentes, cursos),
            MenuApoderados(apoderados),
            MenuPeriodos(periodos),
            MenuEvaluaciones(evaluaciones, asignaturas),
            MenuCalificaciones(NegocioCalificaciones(), estudiantes, evaluaciones),
            MenuAsistencias(NegocioAsistencias(), estudiantes),
            MenuPagos(NegocioPagos(), apoderados),
        ]

    def opciones(self):
        return [(submenu.titulo, submenu.mostrar) for submenu in self.__submenus]

    def mostrar(self):
        # Polimorfismo: redefine mostrar() para agregar los autores al inicio
        # y el mensaje de salida; el resto lo hace la versión de MenuBase.
        print()
        solicitar_datos_autor()
        super().mostrar()
        print('Saliendo del Sistema')
