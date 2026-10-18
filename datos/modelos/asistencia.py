from datos.conexion import base_datos
from peewee import Model, AutoField, DateField, BooleanField, TextField, ForeignKeyField
from datos.modelos.estudiante import Estudiante

database = base_datos()

class BaseModel(Model):
    class Meta:
        database = database

class Asistencia(BaseModel):
    id_asistencia = AutoField()
    fecha = DateField()
    presente = BooleanField()
    observacion = TextField(null=True)
    estudiante = ForeignKeyField(Estudiante, backref='asistencias', null=True)

    class Meta:
        table_name = 'asistencias'
