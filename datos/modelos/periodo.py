from peewee import AutoField, IntegerField, CharField
from datos.modelos.base import BaseModel


class PeriodoAcademico(BaseModel):
    id_periodo = AutoField()
    anio = IntegerField()
    semestre = IntegerField()
    estado = CharField(max_length=30)

    class Meta:
        table_name = 'periodos_academicos'
