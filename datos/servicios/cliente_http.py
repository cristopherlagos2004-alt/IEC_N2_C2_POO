"""Cliente HTTP común para todas las APIs externas (usa la librería requests)."""
import time

import requests

from datos.servicios.errores_servicio import (
    ErrorConfiguracion, ErrorConexionServicio, ErrorTiempoEspera, ErrorSolicitud,
    ErrorCredencialesApi, ErrorNoEncontrado, ErrorLimiteConsultas, ErrorServidorApi,
    ErrorRespuestaInvalida, ErrorServicioExterno, registrar_error_servicio)

# (segundos para conectarse, segundos para recibir la respuesta).
# Sin timeout, requests puede quedarse esperando para siempre y el programa se "congela".
TIEMPO_ESPERA = (4, 10)
INTENTOS = 2                 # 1 intento + 1 reintento (más reintentos dejarían al usuario esperando mucho)
ESPERA_ENTRE_INTENTOS = 1    # segundos; se duplica en cada reintento
ESPERA_MAXIMA = 5            # tope para el encabezado Retry-After
CODIGOS_REINTENTABLES = {429, 500, 502, 503, 504}


class ClienteHttp:
    """Hace solicitudes GET a una API y devuelve el JSON ya convertido a diccionario.

    Se encarga de todo lo que es igual para cualquier API:
    - timeout en cada solicitud
    - reintentos ante fallas pasajeras (sin internet, 429, 5xx)
    - revisar el código HTTP y lanzar un error distinto para cada caso
    - registrar el error en errores.log sin exponer la llave de la API

    Encapsulamiento: el nombre, la URL base y la sesión HTTP son privados.
    """

    def __init__(self, nombre_servicio, url_base, sesion_http=None, esperar=time.sleep):
        if not url_base.startswith('https://'):
            # Solo HTTPS: por HTTP la llave y los datos viajarían sin cifrar
            raise ErrorConfiguracion()
        self.__nombre = nombre_servicio
        self.__url_base = url_base.rstrip('/')
        self.__http = sesion_http or self._crear_sesion()
        self.__esperar = esperar  # se puede reemplazar en las pruebas para no esperar de verdad

    @property
    def nombre(self):
        return self.__nombre

    @staticmethod
    def _crear_sesion():
        """requests.Session reutiliza la conexión entre consultas (más rápido)."""
        sesion = requests.Session()
        sesion.headers.update({'Accept': 'application/json',
                               'User-Agent': 'GestionEscolar-INACAP/3.0'})
        return sesion

    def obtener_json(self, ruta, parametros=None, mensaje_no_encontrado=None):
        """GET a url_base + ruta. Devuelve el JSON como dict o lanza ErrorServicioExterno."""
        url = f'{self.__url_base}/{ruta.lstrip("/")}'
        # Nota: `raise ... from None` corta la cadena de excepciones. Así el error
        # original de requests (que trae la URL con la llave) no queda pegado al nuestro.
        for intento in range(1, INTENTOS + 1):
            ultimo = intento == INTENTOS
            try:
                respuesta = self.__http.get(url, params=parametros, timeout=TIEMPO_ESPERA)
            except requests.exceptions.Timeout as error:
                if not ultimo:
                    self._esperar_reintento(intento)
                    continue
                registrar_error_servicio(self.__nombre, 'sin respuesta (timeout)', error)
                raise ErrorTiempoEspera() from None
            except requests.exceptions.ConnectionError as error:
                # También incluye errores de certificado SSL (SSLError es hija de ConnectionError)
                if not ultimo:
                    self._esperar_reintento(intento)
                    continue
                registrar_error_servicio(self.__nombre, 'error de conexión', error)
                raise ErrorConexionServicio() from None
            except requests.exceptions.RequestException as error:
                # Cualquier otro error de requests (URL inválida, etc.): no se reintenta
                registrar_error_servicio(self.__nombre, 'error en la solicitud', error)
                raise ErrorServicioExterno() from None

            if respuesta.status_code in CODIGOS_REINTENTABLES and not ultimo:
                self._esperar_reintento(intento, respuesta.headers.get('Retry-After'))
                continue
            self._revisar_codigo(respuesta, mensaje_no_encontrado)
            return self._leer_json(respuesta)

    def _esperar_reintento(self, intento, retry_after=None):
        segundos = ESPERA_ENTRE_INTENTOS * 2 ** (intento - 1)  # 1, 2, 4...
        if retry_after and retry_after.isdigit():
            # 429: la API dice cuánto esperar (con un tope, para no congelar el menú)
            segundos = min(int(retry_after), ESPERA_MAXIMA)
        self.__esperar(segundos)

    def _revisar_codigo(self, respuesta, mensaje_no_encontrado):
        """Lanza un error distinto según el código HTTP. 200 = todo bien."""
        codigo = respuesta.status_code
        if codigo == 200:
            return
        registrar_error_servicio(self.__nombre, f'respondió HTTP {codigo}')
        if codigo == 400:
            raise ErrorSolicitud()
        if codigo in (401, 403):
            raise ErrorCredencialesApi()
        if codigo == 404:
            raise ErrorNoEncontrado(mensaje_no_encontrado)
        if codigo == 429:
            raise ErrorLimiteConsultas()
        if 500 <= codigo <= 599:
            raise ErrorServidorApi()
        raise ErrorServicioExterno()  # cualquier otro código (3xx, 418, etc.)

    def _leer_json(self, respuesta):
        tipo = respuesta.headers.get('Content-Type', '')
        if 'json' not in tipo.lower():
            registrar_error_servicio(self.__nombre, f'respuesta no es JSON ({tipo[:50]})')
            raise ErrorRespuestaInvalida()
        try:
            datos = respuesta.json()
        except ValueError:  # requests.JSONDecodeError es hija de ValueError
            registrar_error_servicio(self.__nombre, 'JSON mal formado')
            raise ErrorRespuestaInvalida() from None
        if not isinstance(datos, dict):
            registrar_error_servicio(self.__nombre, 'el JSON no es un objeto')
            raise ErrorRespuestaInvalida()
        return datos
