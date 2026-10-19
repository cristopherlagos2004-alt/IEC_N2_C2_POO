from peewee import AutoField, CharField, DateField, DecimalField, ForeignKeyField
from datos.auxiliares.calculos import promedio_notas
from datos.auxiliares.formatos import formatear_fecha, formatear_nota, formatear_porcentaje
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

    @classmethod
    def columnas(cls):
        return ['Id', 'Nombre', 'Fecha', 'Ponderación', 'Asignatura', 'Promedio']

    def fila(self):
        return [self.id_evaluacion, self.nombre, formatear_fecha(self.fecha),
                formatear_porcentaje(self.porcentaje),
                self.asignatura.descripcion() if self.asignatura else '-',
                formatear_nota(self.calcular_promedio())]

    def descripcion(self):
        asignatura = f' ({self.asignatura.nombre})' if self.asignatura else ''
        return f'{self.nombre}{asignatura}'

    # ----- Métodos del diagrama UML -----

    def calcular_promedio(self):  # UML: calcularPromedio()
        """Promedio del curso en esta evaluación (None si aún no hay notas)."""
        return promedio_notas(c.nota for c in self.calificaciones)
