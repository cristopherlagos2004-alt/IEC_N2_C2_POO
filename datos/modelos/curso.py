from peewee import AutoField, CharField, IntegerField, ForeignKeyField
from datos.modelos.base import BaseModel
from datos.modelos.periodo import PeriodoAcademico


class Curso(BaseModel):
    id_curso = AutoField()
    nombre = CharField(max_length=50)
    nivel = IntegerField()
    jornada = CharField(max_length=30)
    # UML: un Periodo Académico tiene muchos Cursos (1 a *)
    periodo = ForeignKeyField(PeriodoAcademico, column_name='id_periodo',
                              backref='cursos', null=True)

    class Meta:
        table_name = 'cursos'
