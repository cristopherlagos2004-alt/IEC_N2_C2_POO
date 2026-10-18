from datos.conexion import base_datos
from peewee import Model, AutoField, IntegerField, CharField

database = base_datos()

class BaseModel(Model):
    class Meta:
        database = database

class PeriodicoAcademico(BaseModel):
    id_periodico = AutoField()
    anio = IntegerField()
    semestre = IntegerField()
    estado = CharField(max_length=30)

    class Meta:
        table_name = 'periodicos_academicos'
