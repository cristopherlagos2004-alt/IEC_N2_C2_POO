from peewee import AutoField, CharField
from datos.modelos.base import BaseModel


class Apoderado(BaseModel):
    id_apoderado = AutoField()
    nombre = CharField(max_length=100)
    rut = CharField(max_length=15, unique=True)
    telefono = CharField(max_length=20, null=True)
    # La relación con Estudiante ahora está en el modelo Estudiante:
    # UML: un Apoderado tiene muchos Estudiantes (1 a *).

    class Meta:
        table_name = 'apoderados'
