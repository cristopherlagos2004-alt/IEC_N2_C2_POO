from datos.auxiliares.validaciones import validar_monto, validar_opcion
from datos.modelos import ESTADOS_PAGO
from datos.repositorio.repositorio_pagos import RepositorioPagos
from negocio.negocio_base import NegocioBase


class NegocioPagos(NegocioBase):
    nombre_entidad = 'el pago'
    estados = ESTADOS_PAGO
    validadores = {
        'monto': validar_monto,
        'estado': lambda texto: validar_opcion(texto, 'El estado', ESTADOS_PAGO),
    }
    relaciones_obligatorias = {'apoderado': 'Debe seleccionar un apoderado.'}

    def __init__(self, repositorio=None):
        super().__init__(repositorio or RepositorioPagos())

    def registrar_pago(self, pago):
        """Usa el método registrar_pago() del modelo (UML). Devuelve (exito, mensaje)."""
        try:
            pago.registrar_pago()
        except ValueError as error:
            return False, str(error)
        self.repositorio.guardar(pago)
        return True, f'Pago {pago.get_id()} de {pago.apoderado.nombre} marcado como pagado.'
