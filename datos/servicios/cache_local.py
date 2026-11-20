"""Persistencia local de las últimas respuestas válidas de las APIs (archivo JSON).

Si la API no responde, el sistema puede seguir funcionando con el último valor
conocido, avisando al usuario de qué fecha es (continuidad operativa).
"""
import json
import os
from pathlib import Path

from datos.servicios.errores_servicio import registrar_error_servicio

RUTA_POR_DEFECTO = Path(__file__).resolve().parent.parent / 'cache' / 'indicadores.json'


class CacheLocal:
    """Guarda y lee un diccionario {clave: datos} en un archivo JSON."""

    def __init__(self, ruta=RUTA_POR_DEFECTO):
        self.__ruta = Path(ruta)

    def leer(self, clave):
        """Devuelve los datos guardados de esa clave, o None si no hay o el archivo está dañado."""
        contenido = self._leer_todo()
        datos = contenido.get(clave)
        return datos if isinstance(datos, dict) else None

    def guardar(self, clave, datos):
        contenido = self._leer_todo()
        contenido[clave] = datos
        try:
            self.__ruta.parent.mkdir(parents=True, exist_ok=True)
            # Se escribe primero en un archivo temporal y después se reemplaza:
            # si el programa se corta a la mitad, el archivo anterior no queda dañado.
            temporal = self.__ruta.with_suffix('.tmp')
            temporal.write_text(json.dumps(contenido, ensure_ascii=False, indent=2),
                                encoding='utf-8')
            os.replace(temporal, self.__ruta)
        except OSError as error:
            # Si no se puede guardar la caché, el sistema sigue igual (no es crítico)
            registrar_error_servicio('caché local', 'no se pudo guardar', error)

    def _leer_todo(self):
        try:
            contenido = json.loads(self.__ruta.read_text(encoding='utf-8'))
        except FileNotFoundError:
            return {}
        except (OSError, ValueError) as error:
            registrar_error_servicio('caché local', 'archivo ilegible', error)
            return {}
        return contenido if isinstance(contenido, dict) else {}
