from datos.auxiliares.validaciones import validar_nota, validar_fecha_hasta_hoy, validar_texto
from datos.repositorio.repositorio_calificaciones import RepositorioCalificaciones
from negocio.negocio_base import NegocioBase


class NegocioCalificaciones(NegocioBase):
    nombre_entidad = 'la calificación'
    validadores = {
        'nota': validar_nota,
        'fechaRegistro': lambda texto: validar_fecha_hasta_hoy(texto, 'La fecha de registro'),
        'observacion': lambda texto: validar_texto(texto, 'La observación', 255,
                                                   obligatorio=False),
    }
    relaciones_obligatorias = {
        'estudiante': 'Debe seleccionar un estudiante.',
        'evaluacion': 'Debe seleccionar una evaluación.',
    }

    def __init__(self, repositorio=None):
        super().__init__(repositorio or RepositorioCalificaciones())

    def _verificar_reglas(self, datos, actual=None):
        if self.repositorio.existe_calificacion(datos['estudiante'], datos['evaluacion'],
                                                self._id(actual)):
            raise ValueError('Ese estudiante ya tiene nota en esa evaluación. '
                             'Use "Actualizar" para cambiarla.')
