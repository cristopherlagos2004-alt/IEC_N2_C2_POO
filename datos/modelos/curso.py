from datos.conexion import base_datos
from peewee import Model, AutoField, CharField, IntegerField

database = base_datos()

class BaseModel(Model):
    class Meta:
        database = database

class Curso(BaseModel):
    id_curso = AutoField()
    nombre = CharField(max_length=50)
    nivel = IntegerField()
    jornada = CharField(max_length=30)

    class Meta:
        table_name = 'cursos'
