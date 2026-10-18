from peewee import AutoField, DecimalField, DateField, CharField, ForeignKeyField
from datos.modelos.base import BaseModel
from datos.modelos.estudiante import Estudiante
from datos.modelos.evaluacion import Evaluacion


class Calificacion(BaseModel):
    id_calificacion = AutoField()
    nota = DecimalField(max_digits=2, decimal_places=1)  # 1.0 a 7.0
    fechaRegistro = DateField(null=True)
    observacion = CharField(max_length=255, null=True)
    estudiante = ForeignKeyField(Estudiante, column_name='id_estudiante',
                                 backref='calificaciones', null=True)
    # UML: una Evaluación tiene muchas Calificaciones (1 a *)
    evaluacion = ForeignKeyField(Evaluacion, column_name='id_evaluacion',
                                 backref='calificaciones', null=True)

    class Meta:
        table_name = 'calificaciones'
