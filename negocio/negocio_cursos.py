from datos.auxiliares.validaciones import validar_texto, validar_entero, validar_opcion
from datos.modelos import JORNADAS
from datos.repositorio.repositorio_cursos import RepositorioCursos
from negocio.negocio_base import NegocioBase


class NegocioCursos(NegocioBase):
    nombre_entidad = 'el curso'
    jornadas = JORNADAS
    validadores = {
        'nombre': lambda texto: validar_texto(texto, 'El nombre', 50),
        'nivel': lambda texto: validar_entero(texto, 'El nivel', 1, 12),
        'jornada': lambda texto: validar_opcion(texto, 'La jornada', JORNADAS),
    }

    def __init__(self, repositorio=None):
        super().__init__(repositorio or RepositorioCursos())

    def _verificar_reglas(self, datos, actual=None):
        if self.repositorio.existe_nombre(datos['nombre'], datos['periodo'], self._id(actual)):
            raise ValueError(f'Ya existe el curso {datos["nombre"]} en ese periodo.')

    def estudiantes_del_curso(self, curso):
        return self.repositorio.ejecutar(curso.listar_estudiantes)
