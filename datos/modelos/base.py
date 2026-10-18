from peewee import Model
from datos.conexion import base_datos


class BaseModel(Model):
    """Clase padre de todos los modelos: comparten la misma conexión."""
    class Meta:
        database = base_datos
