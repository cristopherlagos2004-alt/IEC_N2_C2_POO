from abc import ABC, abstractmethod
from negocio.negocio_base import ErrorDatos, registrar_error
from presentacion.consola import mostrar_titulo, OperacionCancelada


class MenuBase(ABC):
    """Menú de consola genérico: muestra opciones numeradas y ejecuta la elegida.

    Abstracción: es abstracta; cada menú hijo solo dice QUÉ opciones tiene
    (método opciones()) y esta clase se encarga de CÓMO mostrarlas.
    Encapsulamiento: el título y el texto de salida son atributos privados.
    """

    def __init__(self, titulo, texto_salida='Volver'):
        self.__titulo = titulo
        self.__texto_salida = texto_salida

    @property
    def titulo(self):
        return self.__titulo

    @abstractmethod
    def opciones(self):
        """Lista de pares (texto de la opción, función que se ejecuta)."""

    def mostrar(self):
        while True:
            mostrar_titulo(self.titulo)
            opciones = self.opciones()
            for numero, (texto, _) in enumerate(opciones, start=1):
                print(f'[{numero}] - {texto}')
            print(f'[0] - {self.__texto_salida}')

            eleccion = input(f'Ingrese una opción [0-{len(opciones)}]: ').strip()
            if eleccion == '0':
                break
            if not eleccion.isdigit() or not 1 <= int(eleccion) <= len(opciones):
                print('Opción ingresada NO corresponde. Ingrese nuevamente.')
                continue
            _, accion = opciones[int(eleccion) - 1]
            self._ejecutar(accion)

    @staticmethod
    def _ejecutar(accion):
        """Ejecuta la opción elegida sin que un error cierre el programa."""
        try:
            accion()
        except (ErrorDatos, OperacionCancelada) as error:
            print(error)
        except Exception as error:  # último recurso: se registra y se sigue
            registrar_error(error)
            print('Ocurrió un error inesperado. Revise el archivo errores.log.')
