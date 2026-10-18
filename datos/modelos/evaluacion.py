from datos.conexion import base_datos
from peewee import Model, AutoField, CharField, DateField, FloatField, ForeignKeyField
from datos.modelos.asignatura import Asignatura

database = base_datos()

class BaseModel(Model):
    class Meta:
        database = database

class Evaluacion(BaseModel):
    id_evaluacion = AutoField()
    nombre = CharField(max_length=100)
    fecha = DateField(null=True)
    porcentaje = FloatField()
    asignatura = ForeignKeyField(Asignatura, backref='evaluaciones', null=True)

    class Meta:
        table_name = 'evaluaciones'
