"""Indicadores económicos de Chile desde la API pública de mindicador.cl.

Documentación: https://mindicador.cl  (no necesita llave de acceso)
Ejemplo de respuesta de https://mindicador.cl/api/dolar  (resumida):

    {
      "codigo": "dolar",
      "nombre": "Dólar observado",
      "unidad_medida": "Pesos",
      "serie": [
        {"fecha": "2026-11-20T03:00:00.000Z", "valor": 945.32},
        {"fecha": "2026-11-19T03:00:00.000Z", "valor": 948.10},
        ...
      ]
    }

De todo eso solo usamos: el nombre, y la fecha y el valor más recientes
que no sean de un día futuro.
"""
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation

from auxiliares.validaciones import validar_moneda
from datos.servicios.cache_local import CacheLocal
from datos.servicios.cliente_http import ClienteHttp
from datos.servicios.errores_servicio import (ERRORES_TEMPORALES, ErrorRespuestaInvalida,
                                              registrar_error_servicio)

URL_MINDICADOR = 'https://mindicador.cl/api'
NOMBRES = {'uf': 'UF', 'dolar': 'Dólar', 'euro': 'Euro', 'utm': 'UTM'}


@dataclass(frozen=True)
class Indicador:
    """Valor de un indicador en pesos chilenos. frozen=True: no se puede modificar."""
    codigo: str
    nombre: str
    valor: Decimal       # pesos chilenos por 1 unidad (ej: 1 dólar = 945.32 pesos)
    fecha: date
    desde_cache: bool = False  # True si la API falló y se usó el último valor guardado


class ServicioIndicadores:
    def __init__(self, cliente=None, cache=None, hoy=date.today):
        self.__cliente = cliente or ClienteHttp('mindicador.cl', URL_MINDICADOR)
        self.__cache = cache or CacheLocal()
        self.__hoy = hoy

    def obtener(self, moneda):
        """Devuelve el Indicador de hoy (o el último disponible).

        Si la API falla por algo pasajero (sin internet, timeout, 5xx...) y hay
        un valor guardado, devuelve ese valor marcado con desde_cache=True.
        """
        codigo = validar_moneda(moneda)  # lista blanca: nunca llega otra cosa a la URL
        try:
            datos = self.__cliente.obtener_json(
                codigo, mensaje_no_encontrado='El indicador no está disponible.')
            indicador = self._extraer(codigo, datos)
        except ERRORES_TEMPORALES:
            guardado = self._desde_cache(codigo)
            if guardado is None:
                raise
            return guardado
        self._guardar_en_cache(indicador)
        return indicador

    def _extraer(self, codigo, datos):
        """Saca de la respuesta solo lo necesario y revisa que tenga sentido."""
        try:
            serie = datos['serie']
            if not isinstance(serie, list) or not serie:
                raise ValueError('serie vacía')
            hoy = self.__hoy()
            for registro in serie:  # vienen ordenados del más nuevo al más antiguo
                fecha = date.fromisoformat(str(registro['fecha'])[:10])  # '2026-11-20T03:...'
                if fecha <= hoy:  # se descartan valores de días futuros
                    break
            else:
                raise ValueError('no hay valores hasta hoy')
            valor_original = registro['valor']
            if isinstance(valor_original, bool) or not isinstance(valor_original, (int, float)):
                raise ValueError('el valor no es un número')
            # Decimal(str(...)) y no Decimal(float): evita arrastrar errores del float
            valor = Decimal(str(valor_original))
        except (KeyError, TypeError, ValueError, InvalidOperation) as error:
            registrar_error_servicio('mindicador.cl', f'formato inesperado en "{codigo}"', error)
            raise ErrorRespuestaInvalida() from None
        if not valor.is_finite() or valor <= 0:
            registrar_error_servicio('mindicador.cl', f'valor fuera de rango en "{codigo}"')
            raise ErrorRespuestaInvalida()
        return Indicador(codigo, NOMBRES[codigo], valor, fecha)

    def _guardar_en_cache(self, indicador):
        self.__cache.guardar(indicador.codigo, {'valor': str(indicador.valor),
                                                'fecha': indicador.fecha.isoformat()})

    def _desde_cache(self, codigo):
        guardado = self.__cache.leer(codigo)
        if guardado is None:
            return None
        try:
            valor = Decimal(guardado['valor'])
            fecha = date.fromisoformat(guardado['fecha'])
        except (KeyError, TypeError, ValueError, InvalidOperation):
            return None  # caché dañada: se trata como si no existiera
        if not valor.is_finite() or valor <= 0:
            return None
        return Indicador(codigo, NOMBRES[codigo], valor, fecha, desde_cache=True)
