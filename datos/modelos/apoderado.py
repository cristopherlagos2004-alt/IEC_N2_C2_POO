from datos.conexion import base_datos
from peewee import Model, AutoField, CharField, ForeignKeyField
from datos.modelos.estudiante import Estudiante

database = base_datos()

class BaseModel(Model):
    class Meta:
        database = database

class Apoderado(BaseModel):
    id_apoderado = AutoField()
    nombre = CharField(max_length=100)
    rut = CharField(max_length=15, unique=True)
    telefono = CharField(max_length=20, null=True)
    estudiante = ForeignKeyField(Estudiante, backref='apoderados', null=True)

    class Meta:
        table_name = 'apoderados'
