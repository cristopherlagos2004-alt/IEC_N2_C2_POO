from datos.conexion import base_datos
from peewee import Model, AutoField, FloatField, DateField, TextField, ForeignKeyField
from datos.modelos.estudiante import Estudiante
from datos.modelos.evaluacion import Evaluacion

database = base_datos()

class BaseModel(Model):
    class Meta:
        database = database

class Calificacion(BaseModel):
    id_calificacion = AutoField()
    nota = FloatField()
    fechaRegistro = DateField(null=True)
    observacion = TextField(null=True)
    estudiante = ForeignKeyField(Estudiante, backref='calificaciones', null=True)
    evaluacion = ForeignKeyField(Evaluacion, backref='calificaciones', null=True)

    class Meta:
        table_name = 'calificaciones'
