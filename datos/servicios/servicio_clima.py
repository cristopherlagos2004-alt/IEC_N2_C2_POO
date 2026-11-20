"""Clima actual desde la API de OpenWeatherMap (necesita llave de acceso).

Documentación: https://openweathermap.org/current
La llave se obtiene gratis creando una cuenta en openweathermap.org y se guarda
en el archivo .env como OPENWEATHER_API_KEY. Nunca va escrita en el código.

Ejemplo de respuesta de /data/2.5/weather?q=Temuco,CL&units=metric&lang=es (resumida):

    {
      "weather": [{"id": 500, "main": "Rain", "description": "lluvia ligera"}],
      "main": {"temp": 12.4, "feels_like": 11.8, "humidity": 87},
      "wind": {"speed": 4.1},
      "sys": {"country": "CL"},
      "name": "Temuco"
    }
"""
import re
from dataclasses import dataclass

from datos.auxiliares.validaciones import validar_ciudad, validar_codigo_pais
from datos.servicios.cliente_http import ClienteHttp
from datos.servicios.errores_servicio import (ErrorConfiguracion, ErrorRespuestaInvalida,
                                              registrar_error_servicio)

URL_OPENWEATHER = 'https://api.openweathermap.org/data/2.5'
PATRON_LLAVE = re.compile(r'^[0-9a-f]{32}$')  # las llaves de OpenWeatherMap: 32 caracteres hex


@dataclass(frozen=True)
class Clima:
    ciudad: str
    pais: str
    temperatura: float   # °C
    sensacion: float     # °C
    humedad: int         # %
    viento: float        # m/s
    descripcion: str     # en español, ej: "lluvia ligera"
    codigo_condicion: int  # 2xx tormenta, 3xx llovizna, 5xx lluvia, 6xx nieve, 7xx niebla, 800 despejado


def leer_llave_api():
    """Lee la llave del .env. Lanza ErrorConfiguracion si falta o no tiene el formato correcto."""
    from decouple import config  # se importa aquí para que el resto funcione aunque falte
    llave = config('OPENWEATHER_API_KEY', default='').strip()
    if not PATRON_LLAVE.match(llave):
        registrar_error_servicio('OpenWeatherMap', 'OPENWEATHER_API_KEY falta o no es válida')
        raise ErrorConfiguracion('Falta configurar la llave del servicio de clima en el .env.')
    return llave


class ServicioClima:
    def __init__(self, cliente=None, llave=None):
        self.__cliente = cliente or ClienteHttp('OpenWeatherMap', URL_OPENWEATHER)
        self.__llave = llave  # privada; si es None se lee del .env en la primera consulta

    def obtener(self, ciudad, pais='CL'):
        """Clima actual de la ciudad. Valida los datos antes de llamar a la API."""
        ciudad = validar_ciudad(ciudad)
        pais = validar_codigo_pais(pais)
        if self.__llave is None:
            self.__llave = leer_llave_api()
        parametros = {'q': f'{ciudad},{pais}', 'appid': self.__llave,
                      'units': 'metric', 'lang': 'es'}
        # requests codifica los parámetros (espacios, tildes, &...), así que
        # el texto del usuario no puede romper ni cambiar la URL
        datos = self.__cliente.obtener_json(
            'weather', parametros,
            mensaje_no_encontrado=f'No se encontró la ciudad "{ciudad}" en el país {pais}.')
        return self._extraer(datos, pais)

    @staticmethod
    def _extraer(datos, pais):
        """Saca solo los datos necesarios y revisa tipos y rangos."""
        try:
            principal = datos['main']
            condicion = datos['weather'][0]
            clima = Clima(
                ciudad=str(datos['name'])[:60],
                pais=str(datos.get('sys', {}).get('country', pais))[:2],
                temperatura=float(principal['temp']),
                sensacion=float(principal['feels_like']),
                humedad=int(principal['humidity']),
                viento=float(datos.get('wind', {}).get('speed', 0)),
                descripcion=str(condicion['description'])[:60],
                codigo_condicion=int(condicion['id']),
            )
        except (KeyError, IndexError, TypeError, ValueError, AttributeError) as error:
            registrar_error_servicio('OpenWeatherMap', 'formato inesperado', error)
            raise ErrorRespuestaInvalida() from None
        # Valores imposibles = respuesta dañada (no se usan para decidir nada)
        if not (-90 <= clima.temperatura <= 60 and 0 <= clima.humedad <= 100
                and 0 <= clima.viento <= 120 and 200 <= clima.codigo_condicion <= 899):
            registrar_error_servicio('OpenWeatherMap', 'valores fuera de rango')
            raise ErrorRespuestaInvalida()
        return clima
