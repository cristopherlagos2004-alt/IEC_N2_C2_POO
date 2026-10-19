from peewee import AutoField, CharField, DateField, BooleanField, ForeignKeyField
from datos.auxiliares.calculos import promedio_notas, porcentaje
from datos.auxiliares.formatos import formatear_fecha
from datos.modelos.persona import Persona
from datos.modelos.curso import Curso
from datos.modelos.apoderado import Apoderado


class Estudiante(Persona):
    """Hereda de Persona el atributo nombre y el método mostrar_datos()."""
    id_estudiante = AutoField()
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

    @classmethod
    def columnas(cls):
        return ['Id', 'RUT', 'Nombre', 'Fecha Nacimiento', 'Curso', 'Apoderado']

    def fila(self):
        return [self.id_estudiante, self.rut, self.nombre,
                formatear_fecha(self.fecha_nacimiento),
                self.curso.nombre if self.curso else '-',
                self.apoderado.nombre if self.apoderado else '-']

    def tipo(self):
        return 'Estudiante'

    def mostrar_datos(self):
        # Polimorfismo: usa la versión de Persona y le agrega datos propios
        return (f'{super().mostrar_datos()}\n'
                f'RUT: {self.rut}\n'
                f'Fecha de nacimiento: {formatear_fecha(self.fecha_nacimiento)}\n'
                f'Curso: {self.curso.nombre if self.curso else "-"}\n'
                f'Apoderado: {self.apoderado.nombre if self.apoderado else "-"}')

    # ----- Métodos del diagrama UML -----

    def consultar_notas(self):  # UML: consultarNotas()
        return sorted(self.calificaciones, key=lambda c: c.id_calificacion)

    def consultar_asignaturas(self):  # UML: consultarAsignaturas()
        """Asignaturas del curso del estudiante."""
        return sorted(self.curso.asignaturas, key=lambda a: a.nombre) if self.curso else []

    def obtener_promedio(self):  # UML: obtenerPromedio()
        """Promedio simple de todas sus notas (None si no tiene notas)."""
        return promedio_notas(c.nota for c in self.calificaciones)

    def obtener_porcentaje_asistencia(self):  # UML de Asistencia: obtenerPorcentajeAsistencia()
        """Porcentaje de clases en que estuvo presente (None si no hay registros)."""
        registros = list(self.asistencias)
        presentes = sum(1 for a in registros if a.presente)
        return porcentaje(presentes, len(registros))
