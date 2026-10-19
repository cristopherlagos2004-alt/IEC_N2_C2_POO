"""Manejo centralizado de errores de la base de datos."""
import logging

MENSAJE_GENERAL = 'Ocurrió un error con la base de datos. Revise el archivo errores.log.'
MENSAJE_INTEGRIDAD = ('No se pudo completar la operación: el dato está repetido '
                      'o hay otros registros que dependen de este.')

# El detalle técnico se guarda en errores.log y NO se muestra en pantalla,
# para no exponer información interna de la base de datos.
# delay=True: el archivo solo se crea cuando ocurre el primer error.
_manejador = logging.FileHandler('errores.log', encoding='utf-8', delay=True)
_manejador.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
_logger = logging.getLogger('gestion_escolar')
_logger.setLevel(logging.ERROR)
_logger.addHandler(_manejador)


class ErrorDatos(Exception):
    """Error de la capa de datos con un mensaje apto para mostrar al usuario."""


def registrar_error(error):
    """Guarda el detalle técnico del error en errores.log."""
    _logger.error('Error de base de datos: %s', error, exc_info=error)
