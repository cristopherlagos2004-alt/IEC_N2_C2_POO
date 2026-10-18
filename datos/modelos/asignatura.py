from peewee import AutoField, CharField, IntegerField, ForeignKeyField
from datos.modelos.base import BaseModel
from datos.modelos.docente import Docente
from datos.modelos.curso import Curso


class Asignatura(BaseModel):
    id_asignatura = AutoField()
    nombre = CharField(max_length=50)
    codigo = CharField(max_length=20)
    horasSemanales = IntegerField()
    # UML: un Docente imparte muchas Asignaturas (1 a *)
    docente = ForeignKeyField(Docente, column_name='id_docente',
                              backref='asignaturas', null=True)
    # UML: un Curso tiene muchas Asignaturas (1 a *)
    curso = ForeignKeyField(Curso, column_name='id_curso',
                            backref='asignaturas', null=True)

    class Meta:
        table_name = 'asignaturas'
