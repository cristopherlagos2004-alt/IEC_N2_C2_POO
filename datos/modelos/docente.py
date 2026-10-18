from peewee import AutoField, CharField
from datos.modelos.base import BaseModel


class Docente(BaseModel):
    id_docente = AutoField()
    nombre = CharField(max_length=100)
    correo = CharField(max_length=100, null=True)
    especialidad = CharField(max_length=100, null=True)

    class Meta:
        table_name = 'docentes'
