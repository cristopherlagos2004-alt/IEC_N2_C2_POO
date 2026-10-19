from peewee import AutoField, CharField, IntegerField, ForeignKeyField
from datos.modelos.base import BaseModel
from datos.modelos.periodo import PeriodoAcademico

JORNADAS = ('Mañana', 'Tarde', 'Completa')


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

    @classmethod
    def columnas(cls):
        return ['Id', 'Nombre', 'Nivel', 'Jornada', 'Periodo', 'N° Estudiantes']

    def fila(self):
        return [self.id_curso, self.nombre, self.nivel, self.jornada,
                self.periodo.descripcion() if self.periodo else '-',
                self.consultar_cantidad_estudiantes()]

    def descripcion(self):
        return self.nombre

    # ----- Métodos del diagrama UML -----

    def listar_estudiantes(self):  # UML: listarEstudiantes()
        """Estudiantes activos del curso (los eliminados no aparecen)."""
        return sorted((e for e in self.estudiantes if e.activo), key=lambda e: e.nombre)

    def consultar_cantidad_estudiantes(self):  # UML: consultarCantidadEstudiantes()
        return len(self.listar_estudiantes())
