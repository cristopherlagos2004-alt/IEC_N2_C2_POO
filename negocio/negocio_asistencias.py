from datos.auxiliares.validaciones import validar_fecha_hasta_hoy, validar_si_no, validar_texto
from datos.repositorio.repositorio_asistencias import RepositorioAsistencias
from negocio.negocio_base import NegocioBase


class NegocioAsistencias(NegocioBase):
    nombre_entidad = 'la asistencia'
    validadores = {
        'fecha': validar_fecha_hasta_hoy,
        'presente': lambda texto: validar_si_no(texto, '¿Presente?'),
        'observacion': lambda texto: validar_texto(texto, 'La observación', 500,
                                                   obligatorio=False),
    }
    relaciones_obligatorias = {'estudiante': 'Debe seleccionar un estudiante.'}

    def __init__(self, repositorio=None):
        super().__init__(repositorio or RepositorioAsistencias())

    def _verificar_reglas(self, datos, actual=None):
        if self.repositorio.existe_asistencia(datos['estudiante'], datos['fecha'],
                                              self._id(actual)):
            raise ValueError('Ese estudiante ya tiene asistencia registrada ese día.')
