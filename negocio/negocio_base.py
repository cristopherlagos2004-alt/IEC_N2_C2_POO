from abc import ABC, abstractmethod

# La capa de presentación recibe estos errores a través de negocio
# (no importa nada de la capa de datos directamente).
from datos.auxiliares.errores import ErrorDatos, registrar_error  # noqa: F401


class NegocioBase(ABC):
    """Lógica común a todas las entidades: validar los datos y, si están bien,
    pedirle al repositorio que los guarde.

    Abstracción: clase abstracta; cada hija declara sus validadores y sus reglas.
    Encapsulamiento: el repositorio es un atributo privado (__repositorio)
    y solo se puede leer con la propiedad repositorio (no se puede reemplazar).
    Polimorfismo: crear(), actualizar() y eliminar() funcionan igual para todas
    las hijas, pero cada una valida y verifica reglas a su manera.
    """

    # Relaciones con otros registros que no pueden quedar vacías:
    # {campo: mensaje de error}. Las hijas lo redefinen si tienen alguna.
    relaciones_obligatorias = {}

    def __init__(self, repositorio):
        self.__repositorio = repositorio

    @property
    def repositorio(self):
        return self.__repositorio

    @property
    @abstractmethod
    def nombre_entidad(self):
        """Nombre con artículo para los mensajes (ej: 'el estudiante')."""

    @property
    @abstractmethod
    def validadores(self):
        """Diccionario {campo: función} para validar cada dato que escribe el usuario.

        Cada función recibe el texto escrito y devuelve el valor limpio,
        o lanza ValueError con un mensaje para el usuario.
        """

    def _verificar_reglas(self, datos, actual=None):
        """Reglas que necesitan consultar la base de datos (ej: RUT repetido).
        Por defecto no hay ninguna; las hijas la redefinen. Lanza ValueError."""

    # ----- Validación -----

    def validar_campo(self, campo, texto):
        """Valida un solo dato. La presentación lo usa para avisar al tiro si
        algo está mal, sin esperar a que se completen todos los datos."""
        return self.validadores[campo](texto)

    def es_obligatoria(self, relacion):
        return relacion in self.relaciones_obligatorias

    def _validar(self, datos):
        """Valida todos los datos y devuelve un diccionario con los valores limpios."""
        limpios = {}
        for campo, valor in datos.items():
            if campo in self.validadores:
                limpios[campo] = self.validar_campo(campo, valor)
            else:
                # Relación con otro registro: la presentación ya entrega el registro elegido
                if valor is None and self.es_obligatoria(campo):
                    raise ValueError(self.relaciones_obligatorias[campo])
                limpios[campo] = valor
        return limpios

    # ----- Utilidades para las clases hijas -----

    @staticmethod
    def _id(registro):
        return registro.get_id() if registro is not None else None

    def _nombrar(self, registro):
        return f'{self.nombre_entidad} "{registro.descripcion()}"'

    # ----- Operaciones CRUD -----

    def listar(self):
        return self.repositorio.listar()

    def buscar(self, texto):
        return self.repositorio.buscar(texto.strip())

    def obtener(self, id_texto):
        """Devuelve el registro con ese Id, o None si el Id no es válido o no existe."""
        id_texto = str(id_texto).strip()
        if not id_texto.isdigit():
            return None
        return self.repositorio.obtener_por_id(int(id_texto))

    def crear(self, datos):
        """Valida y guarda un registro nuevo. Devuelve (exito, mensaje)."""
        try:
            limpios = self._validar(datos)
            self._verificar_reglas(limpios)
        except ValueError as error:
            return False, str(error)
        registro = self.repositorio.modelo(**limpios)
        self.repositorio.guardar(registro)
        return True, f'Se registró {self._nombrar(registro)} (Id {registro.get_id()}).'

    def actualizar(self, registro, datos):
        """Valida y guarda los cambios de un registro. Devuelve (exito, mensaje)."""
        try:
            limpios = self._validar(datos)
            self._verificar_reglas(limpios, actual=registro)
        except ValueError as error:
            return False, str(error)
        for campo, valor in limpios.items():
            setattr(registro, campo, valor)
        self.repositorio.guardar(registro)
        return True, f'Se actualizó {self._nombrar(registro)}.'

    def eliminar(self, registro):
        """Borra el registro si ningún otro depende de él. Devuelve (exito, mensaje)."""
        dependencias = self.repositorio.contar_dependencias(registro)
        if dependencias:
            detalle = ', '.join(f'{cantidad} en {tabla}' for tabla, cantidad in dependencias)
            return False, (f'No se puede eliminar {self._nombrar(registro)}: tiene registros '
                           f'asociados ({detalle}). Elimínelos o cámbielos primero.')
        nombre = self._nombrar(registro)
        self.repositorio.eliminar(registro)
        return True, f'Se eliminó {nombre}.'
