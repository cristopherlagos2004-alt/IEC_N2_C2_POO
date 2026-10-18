from peewee import AutoField, CharField, DateField, DecimalField, ForeignKeyField
from datos.modelos.base import BaseModel
from datos.modelos.asignatura import Asignatura


class Evaluacion(BaseModel):
    id_evaluacion = AutoField()
    nombre = CharField(max_length=100)
    fecha = DateField(null=True)
    porcentaje = DecimalField(max_digits=5, decimal_places=2)
    # UML: una Asignatura tiene muchas Evaluaciones (1 a *)
    asignatura = ForeignKeyField(Asignatura, column_name='id_asignatura',
                                 backref='evaluaciones', null=True)

    class Meta:
        table_name = 'evaluaciones'
