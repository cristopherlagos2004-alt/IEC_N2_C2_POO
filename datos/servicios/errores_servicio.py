"""Errores al consumir servicios externos (APIs) y su registro seguro.

Jerarquía de excepciones (manejo jerárquico):

    ErrorDatos                      (ya existía: el menú la muestra sin cerrar el programa)
    └── ErrorServicioExterno        cualquier problema con una API
        ├── ErrorConfiguracion      falta la llave de la API en el .env
        ├── ErrorConexionServicio   sin internet / servidor no responde
        ├── ErrorTiempoEspera       la API se demoró más que el timeout
        ├── ErrorSolicitud          400: la consulta está mal armada
        ├── ErrorCredencialesApi    401 / 403: la llave no sirve
        ├── ErrorNoEncontrado       404: ciudad o indicador no existe
        ├── ErrorLimiteConsultas    429: demasiadas consultas
        ├── ErrorServidorApi        500 a 599: falla del lado de la API
        └── ErrorRespuestaInvalida  la respuesta no trae los datos esperados

Así se puede capturar un error específico (ej: solo ErrorTiempoEspera) o
todos juntos (ErrorServicioExterno). El mensaje de cada error es apto para
mostrarlo al usuario: no trae URLs, llaves ni detalles técnicos. El detalle
técnico va a errores.log, con las llaves ocultas.
"""
import re

from datos.auxiliares.errores import ErrorDatos, obtener_logger


class ErrorServicioExterno(ErrorDatos):
    mensaje = 'No se pudo obtener la información del servicio externo.'

    def __init__(self, mensaje=None):
        super().__init__(mensaje or self.mensaje)


class ErrorConfiguracion(ErrorServicioExterno):
    mensaje = 'El servicio externo no está configurado. Avise al administrador.'


class ErrorConexionServicio(ErrorServicioExterno):
    mensaje = 'No hay conexión con el servicio externo. Revise su conexión a internet.'


class ErrorTiempoEspera(ErrorServicioExterno):
    mensaje = 'El servicio externo tardó demasiado en responder. Intente más tarde.'


class ErrorSolicitud(ErrorServicioExterno):
    mensaje = 'El servicio externo no aceptó la consulta. Revise los datos ingresados.'


class ErrorCredencialesApi(ErrorServicioExterno):
    mensaje = 'El servicio externo rechazó la llave de acceso. Avise al administrador.'


class ErrorNoEncontrado(ErrorServicioExterno):
    mensaje = 'El servicio externo no encontró lo que buscaba.'


class ErrorLimiteConsultas(ErrorServicioExterno):
    mensaje = 'Se hicieron demasiadas consultas al servicio externo. Espere un momento.'


class ErrorServidorApi(ErrorServicioExterno):
    mensaje = 'El servicio externo tiene problemas en este momento. Intente más tarde.'


class ErrorRespuestaInvalida(ErrorServicioExterno):
    mensaje = 'El servicio externo respondió con datos que no se pueden usar.'


# Errores en que vale la pena usar datos guardados (caché) o reintentar:
# son problemas pasajeros, no culpa del usuario ni de la configuración.
ERRORES_TEMPORALES = (ErrorConexionServicio, ErrorTiempoEspera,
                      ErrorLimiteConsultas, ErrorServidorApi, ErrorRespuestaInvalida)


# Busca cosas como  appid=abc123  o  api_key=abc123  en un texto.
_PATRON_SECRETO = re.compile(r'(appid|api_?key|key|token|password)=[^&\s\'"]+', re.IGNORECASE)


def ocultar_secretos(texto) -> str:
    """'...?q=Temuco&appid=abc123' -> '...?q=Temuco&appid=***'

    Las excepciones de requests incluyen la URL completa, y la URL del clima
    lleva la llave de la API. Sin esto, la llave quedaría escrita en errores.log.
    """
    return _PATRON_SECRETO.sub(lambda m: f'{m.group(1)}=***', str(texto))


def registrar_error_servicio(servicio, descripcion, error=None):
    """Guarda en errores.log qué pasó, sin llaves ni contraseñas."""
    detalle = f'{type(error).__name__}: {ocultar_secretos(error)}' if error else ''
    obtener_logger().error('Servicio externo [%s] %s %s', servicio, descripcion, detalle)
