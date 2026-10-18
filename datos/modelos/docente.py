from datos.conexion import base_datos
from peewee import Model, AutoField, CharField

database = base_datos()

class BaseModel(Model):
    class Meta:
        database = database

class Docente(BaseModel):
    id_docente = AutoField()
    nombre = CharField(max_length=100)
    correo = CharField(max_length=100, null=True)
    especialidad = CharField(max_length=100, null=True)

    class Meta:
        table_name = 'docentes'
