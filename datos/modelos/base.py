from peewee import Model
from datos.conexion import base_datos


class BaseModel(Model):
    """Clase padre de TODOS los modelos (herencia).

    Define métodos que cada modelo hijo implementa a su manera (polimorfismo):
    así la capa de presentación puede mostrar cualquier modelo en una tabla
    sin saber de qué clase es.
    """

    class Meta:
        database = base_datos

    @classmethod
    def columnas(cls):
        """Títulos de las columnas al mostrar este modelo en una tabla."""
        raise NotImplementedError('Cada modelo debe definir sus columnas.')

    def fila(self):
        """Valores del registro, en el mismo orden que columnas()."""
        raise NotImplementedError('Cada modelo debe definir su fila.')

    def descripcion(self):
        """Texto corto que identifica al registro (ej: '1° Medio A')."""
        raise NotImplementedError('Cada modelo debe definir su descripción.')

    def __str__(self):
        return self.descripcion()
