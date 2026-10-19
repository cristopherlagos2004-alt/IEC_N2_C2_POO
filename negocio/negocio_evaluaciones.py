from decimal import Decimal
from datos.auxiliares.formatos import formatear_porcentaje
from datos.auxiliares.validaciones import validar_texto, validar_fecha, validar_porcentaje
from datos.repositorio.repositorio_evaluaciones import RepositorioEvaluaciones
from negocio.negocio_base import NegocioBase


class NegocioEvaluaciones(NegocioBase):
    nombre_entidad = 'la evaluación'
    validadores = {
        'nombre': lambda texto: validar_texto(texto, 'El nombre', 100),
        'fecha': validar_fecha,
        'porcentaje': validar_porcentaje,
    }
    relaciones_obligatorias = {'asignatura': 'Debe seleccionar una asignatura.'}

    def __init__(self, repositorio=None):
        super().__init__(repositorio or RepositorioEvaluaciones())

    def _verificar_reglas(self, datos, actual=None):
        # Regla de negocio: las ponderaciones de una asignatura no pueden pasar de 100%
        otras = Decimal(str(self.repositorio.suma_porcentajes(datos['asignatura'],
                                                              self._id(actual))))
        total = otras + datos['porcentaje']
        if total > 100:
            raise ValueError(f'Las ponderaciones de la asignatura sumarían {formatear_porcentaje(total)} '
                             f'(máximo 100%). Disponible: {formatear_porcentaje(100 - otras)}.')
