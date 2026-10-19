from datos.auxiliares.validaciones import validar_nombre, validar_correo, validar_texto
from datos.repositorio.repositorio_docentes import RepositorioDocentes
from negocio.negocio_base import NegocioBase


class NegocioDocentes(NegocioBase):
    nombre_entidad = 'el docente'
    validadores = {
        'nombre': validar_nombre,
        'correo': validar_correo,
        'especialidad': lambda texto: validar_texto(texto, 'La especialidad', 100,
                                                    obligatorio=False),
    }

    def __init__(self, repositorio=None):
        super().__init__(repositorio or RepositorioDocentes())

    def ficha(self, docente):
        """Datos del docente, sus asignaturas y sus estudiantes."""
        return self.repositorio.ejecutar(lambda: {
            'datos': docente.mostrar_datos(),
            'asignaturas': docente.consultar_asignaturas(),
            'estudiantes': docente.consultar_estudiantes(),
        })
