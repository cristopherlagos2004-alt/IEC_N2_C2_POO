from datos.conexion import base_datos
from peewee import Model, AutoField, CharField, IntegerField

database = base_datos()

class BaseModel(Model):
    class Meta:
        database = database

class Asignatura(BaseModel):
    id_asignatura = AutoField()
    nombre = CharField(max_length=50)
    codigo = CharField(max_length=20)
    horasSemanales = IntegerField()

    class Meta:
        table_name = 'asignaturas'
