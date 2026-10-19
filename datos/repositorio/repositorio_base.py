from abc import ABC, abstractmethod
from peewee import PeeweeException, IntegrityError
from datos.auxiliares.errores import (ErrorDatos, registrar_error,
                                      MENSAJE_GENERAL, MENSAJE_INTEGRIDAD)


class RepositorioBase(ABC):
    """Operaciones CRUD comunes a todas las tablas.

    Abstracción: es una clase abstracta (no se puede instanciar). Cada repositorio
    hijo solo indica su modelo y hereda listar, obtener, buscar, guardar y eliminar.
    Polimorfismo: los hijos pueden redefinir estos métodos (por ejemplo,
    RepositorioEstudiantes hace eliminación lógica en vez de borrar).
    """

    @property
    @abstractmethod
    def modelo(self):
        """Clase del modelo que maneja este repositorio."""

    # ----- Manejo de errores -----

    def ejecutar(self, operacion):
        """Ejecuta una operación de base de datos.

        Si falla, guarda el detalle en errores.log y lanza ErrorDatos
        con un mensaje que se puede mostrar al usuario.
        """
        try:
            return operacion()
        except IntegrityError as error:
            registrar_error(error)
            raise ErrorDatos(MENSAJE_INTEGRIDAD) from error
        except PeeweeException as error:
            registrar_error(error)
            raise ErrorDatos(MENSAJE_GENERAL) from error

    # ----- Consultas -----

    def _consulta_base(self):
        """Consulta de partida. Los hijos la redefinen para filtrar."""
        return self.modelo.select()

    def _condicion_busqueda(self, texto):
        """Condición para buscar. Por defecto busca por nombre."""
        return self.modelo.nombre.contains(texto)

    def listar(self):
        clave = self.modelo._meta.primary_key
        return self.ejecutar(lambda: list(self._consulta_base().order_by(clave)))

    def obtener_por_id(self, id_registro):
        clave = self.modelo._meta.primary_key
        return self.ejecutar(lambda: self._consulta_base().where(clave == id_registro).first())

    def buscar(self, texto):
        return self.ejecutar(
            lambda: list(self._consulta_base().where(self._condicion_busqueda(texto))))

    def _existe(self, condicion, excluir_id=None):
        """True si hay algún registro que cumple la condición (sin contar excluir_id)."""
        consulta = self.modelo.select().where(condicion)
        if excluir_id is not None:
            consulta = consulta.where(self.modelo._meta.primary_key != excluir_id)
        return self.ejecutar(consulta.exists)

    def contar_dependencias(self, registro):
        """Registros de otras tablas que apuntan a este (ej: asignaturas de un docente).

        Devuelve una lista de (nombre de la tabla, cantidad), solo con las que tienen alguno.
        Sirve para avisar antes de eliminar, en vez de que la base de datos lo rechace.
        """
        def contar():
            resultado = []
            # _meta.backrefs: relaciones de otros modelos que apuntan a este
            for campo, modelo_dependiente in self.modelo._meta.backrefs.items():
                cantidad = modelo_dependiente.select().where(campo == registro).count()
                if cantidad:
                    resultado.append((modelo_dependiente._meta.table_name, cantidad))
            return resultado
        return self.ejecutar(contar)

    # ----- Escritura -----

    def guardar(self, registro):
        self.ejecutar(registro.save)

    def eliminar(self, registro):
        """Eliminación física (borra la fila)."""
        self.ejecutar(registro.delete_instance)
