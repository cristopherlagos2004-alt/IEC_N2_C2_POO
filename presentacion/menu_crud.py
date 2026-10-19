from abc import abstractmethod
from datetime import date
from presentacion.consola import SIN_VALOR, OperacionCancelada, mostrar_tabla, pedir, confirmar
from presentacion.menu_base import MenuBase


class MenuCrud(MenuBase):
    """Menú con las 5 operaciones CRUD: listar, registrar, buscar, actualizar y eliminar.

    Herencia: hereda de MenuBase la forma de mostrar las opciones.
    Abstracción: cada menú hijo solo implementa pedir_datos().
    Polimorfismo: cada hijo puede agregar opciones con opciones_extra().
    Encapsulamiento: la clase de negocio es un atributo privado (__negocio).
    """

    def __init__(self, titulo, negocio):
        super().__init__(titulo)
        self.__negocio = negocio

    @property
    def negocio(self):
        return self.__negocio

    @property
    def texto_busqueda(self):
        """Qué se escribe para buscar. Los hijos lo redefinen si buscan por otra cosa."""
        return 'el nombre'

    @abstractmethod
    def pedir_datos(self, actual=None):
        """Pide los datos del registro. Si viene 'actual', es una actualización."""

    def opciones_extra(self):
        """Opciones propias de cada menú. Por defecto no hay."""
        return []

    def opciones(self):
        return [
            ('Listar', self.listar),
            ('Registrar', self.registrar),
            ('Buscar', self.buscar),
            ('Actualizar', self.actualizar),
            ('Eliminar', self.eliminar),
        ] + self.opciones_extra()

    # ----- Operaciones CRUD -----

    def listar(self):
        mostrar_tabla(self.negocio.listar())

    def registrar(self):
        _, mensaje = self.negocio.crear(self.pedir_datos())
        print(mensaje)

    def buscar(self):
        texto = input(f'Ingrese {self.texto_busqueda} a buscar: ')
        mostrar_tabla(self.negocio.buscar(texto))

    def seleccionar(self, accion):
        """Muestra los registros y pide un Id. Devuelve el registro o None."""
        registros = self.negocio.listar()
        if not registros:
            print('No hay registros.')
            return None
        mostrar_tabla(registros)
        registro = self.negocio.obtener(input(f'Ingrese el Id para {accion}: '))
        if registro is None:
            print('No se encontró un registro con ese Id.')
        return registro

    def actualizar(self):
        registro = self.seleccionar('modificar')
        if registro is None:
            return
        print('ENTER conserva el valor actual; "-" deja vacío un campo opcional.')
        _, mensaje = self.negocio.actualizar(registro, self.pedir_datos(registro))
        print(mensaje)

    def eliminar(self):
        registro = self.seleccionar('eliminar')
        if registro is None:
            return
        if confirmar(f'¿Seguro que desea eliminar "{registro.descripcion()}"?'):
            _, mensaje = self.negocio.eliminar(registro)
            print(mensaje)
        else:
            print('Operación cancelada.')

    # ----- Ayudas para los menús hijos -----

    @staticmethod
    def _valor(actual, campo):
        """Valor actual de un campo para mostrarlo al actualizar (SIN_VALOR si es nuevo)."""
        if actual is None:
            return SIN_VALOR
        valor = getattr(actual, campo)
        if isinstance(valor, bool):
            return 's' if valor else 'n'
        if isinstance(valor, date):
            return valor.strftime('%d-%m-%Y')
        return valor

    def _pedir(self, campo, texto, actual=None):
        """Pide un dato y lo valida al tiro con la capa de negocio.

        Si está mal, muestra el motivo y lo vuelve a pedir; así el usuario no
        tiene que completar todo el formulario para enterarse del error.
        """
        while True:
            valor = pedir(texto, self._valor(actual, campo))
            try:
                self.negocio.validar_campo(campo, valor)
                return valor
            except ValueError as error:
                print(f'  >> {error} Intente nuevamente.')

    def _elegir(self, negocio_relacionado, etiqueta, campo, actual=None):
        """Muestra los registros de otra entidad y pide el Id de uno (para las relaciones).

        Devuelve el registro elegido, o None si se deja vacío (solo si no es obligatorio).
        """
        obligatoria = self.negocio.es_obligatoria(campo)
        relacionado = getattr(actual, campo) if actual is not None else None
        registros = negocio_relacionado.listar()
        if obligatoria and not registros and relacionado is None:
            raise OperacionCancelada(f'No hay registros de "{etiqueta}". '
                                     'Regístrelos primero en su menú.')

        print(f'\n--- {etiqueta.capitalize()} ---')
        mostrar_tabla(registros)
        if actual is None:
            valor_actual = SIN_VALOR
            texto = f'Id de {etiqueta}' + ('' if obligatoria else ' (ENTER = ninguno)')
        else:
            valor_actual = relacionado.get_id() if relacionado is not None else None
            texto = f'Id de {etiqueta}'

        while True:
            id_texto = pedir(texto, valor_actual)
            if id_texto == '':
                if obligatoria:
                    print('  >> Este dato es obligatorio.')
                    continue
                return None
            if relacionado is not None and id_texto == str(relacionado.get_id()):
                # Conserva el actual aunque ya no aparezca en la lista
                # (por ejemplo, un estudiante que fue desactivado)
                return relacionado
            registro = negocio_relacionado.obtener(id_texto)
            if registro is not None:
                return registro
            print(f'  >> No hay ningún registro con Id {id_texto}. Intente nuevamente.')
