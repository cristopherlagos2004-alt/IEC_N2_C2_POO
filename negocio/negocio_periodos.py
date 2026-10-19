from datos.auxiliares.validaciones import validar_entero, validar_opcion
from datos.modelos import ESTADOS_PERIODO
from datos.repositorio.repositorio_periodos import RepositorioPeriodos
from negocio.negocio_base import NegocioBase


class NegocioPeriodos(NegocioBase):
    nombre_entidad = 'el periodo'
    estados = ESTADOS_PERIODO
    validadores = {
        'anio': lambda texto: validar_entero(texto, 'El año', 2000, 2100),
        'semestre': lambda texto: validar_entero(texto, 'El semestre', 1, 2),
        'estado': lambda texto: validar_opcion(texto, 'El estado', ESTADOS_PERIODO),
    }

    def __init__(self, repositorio=None):
        super().__init__(repositorio or RepositorioPeriodos())

    def _verificar_reglas(self, datos, actual=None):
        excluir = self._id(actual)
        if self.repositorio.existe_periodo(datos['anio'], datos['semestre'], excluir):
            raise ValueError(f'Ya existe el periodo {datos["anio"]}-{datos["semestre"]}.')
        self._verificar_unico_activo(datos['estado'], excluir)

    def _verificar_unico_activo(self, estado, excluir_id):
        if estado == 'Activo' and self.repositorio.existe_otro_activo(excluir_id):
            raise ValueError('Ya hay otro periodo Activo. Ciérrelo antes de activar este.')

    def cambiar_estado(self, periodo, nuevo_estado):
        """Usa el método cambiar_estado() del modelo (UML). Devuelve (exito, mensaje)."""
        try:
            estado = self.validar_campo('estado', nuevo_estado)
            self._verificar_unico_activo(estado, periodo.get_id())
            periodo.cambiar_estado(estado)
        except ValueError as error:
            return False, str(error)
        self.repositorio.guardar(periodo)
        return True, f'El periodo {periodo.anio}-{periodo.semestre} quedó {estado}.'
