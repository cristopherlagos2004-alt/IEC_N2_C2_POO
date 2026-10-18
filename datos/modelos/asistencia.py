from peewee import AutoField, DateField, BooleanField, CharField, ForeignKeyField
from datos.modelos.base import BaseModel
from datos.modelos.estudiante import Estudiante


class Asistencia(BaseModel):
    id_asistencia = AutoField()
    fecha = DateField()
    presente = BooleanField(default=True)
    observacion = CharField(max_length=500, null=True)
    # UML: un Estudiante tiene muchas Asistencias (1 a *)
    estudiante = ForeignKeyField(Estudiante, column_name='id_estudiante',
                                 backref='asistencias', null=True)

    class Meta:
        table_name = 'asistencias'
