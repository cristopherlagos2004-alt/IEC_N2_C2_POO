from peewee import AutoField, CharField, DateField, BooleanField, ForeignKeyField
from datos.modelos.base import BaseModel
from datos.modelos.curso import Curso
from datos.modelos.apoderado import Apoderado


class Estudiante(BaseModel):
    id_estudiante = AutoField()
    nombre = CharField(max_length=100)
    rut = CharField(max_length=15, unique=True)
    fecha_nacimiento = DateField(null=True)
    # UML: un Curso tiene muchos Estudiantes (1 a *)
    curso = ForeignKeyField(Curso, column_name='id_curso',
                            backref='estudiantes', null=True)
    # UML: un Apoderado tiene muchos Estudiantes (1 a *)
    apoderado = ForeignKeyField(Apoderado, column_name='id_apoderado',
                                backref='estudiantes', null=True)
    # Eliminación lógica: en vez de borrar el registro se marca como inactivo
    activo = BooleanField(default=True)

    class Meta:
        table_name = 'estudiantes'
