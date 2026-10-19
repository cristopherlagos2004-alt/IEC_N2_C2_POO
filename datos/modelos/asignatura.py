from peewee import AutoField, CharField, IntegerField, ForeignKeyField
from datos.auxiliares.calculos import promedio_notas
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

    @classmethod
    def columnas(cls):
        return ['Id', 'Código', 'Nombre', 'Horas/semana', 'Docente', 'Curso']

    def fila(self):
        return [self.id_asignatura, self.codigo, self.nombre, self.horasSemanales,
                self.docente.nombre if self.docente else '-',
                self.curso.nombre if self.curso else '-']

    def descripcion(self):
        curso = f' - {self.curso.nombre}' if self.curso else ''
        return f'{self.codigo} {self.nombre}{curso}'

    # ----- Métodos del diagrama UML -----

    def listar_estudiantes(self):  # UML: listarEstudiantes()
        """Estudiantes del curso al que pertenece la asignatura."""
        return self.curso.listar_estudiantes() if self.curso else []

    def calcular_promedio(self):  # UML: calcularPromedio()
        """Promedio de todas las notas de todas las evaluaciones de la asignatura."""
        notas = [c.nota for evaluacion in self.evaluaciones for c in evaluacion.calificaciones]
        return promedio_notas(notas)
