from datos.conexion import base_datos
from peewee import Model, AutoField, CharField, DateField, ForeignKeyField
from datos.modelos.curso import Curso

database = base_datos()

class BaseModel(Model):
    class Meta:
        database = database

class Estudiante(BaseModel):
    id_estudiante = AutoField()
    nombre = CharField(max_length=100)
    rut = CharField(max_length=15, unique=True)
    fecha_nacimiento = DateField(null=True)
    curso = ForeignKeyField(Curso, backref='estudiantes', null=True)

    class Meta:
        table_name = 'estudiantes'
