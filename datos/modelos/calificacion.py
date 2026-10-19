from decimal import Decimal
from peewee import AutoField, DecimalField, DateField, CharField, ForeignKeyField
from datos.auxiliares.formatos import formatear_fecha, formatear_nota, texto_o_guion
from datos.modelos.base import BaseModel
from datos.modelos.estudiante import Estudiante
from datos.modelos.evaluacion import Evaluacion

NOTA_MINIMA = Decimal('1.0')
NOTA_MAXIMA = Decimal('7.0')
NOTA_APROBACION = Decimal('4.0')


class Calificacion(BaseModel):
    id_calificacion = AutoField()
    nota = DecimalField(max_digits=2, decimal_places=1)  # 1.0 a 7.0
    fechaRegistro = DateField(null=True)
    observacion = CharField(max_length=255, null=True)
    estudiante = ForeignKeyField(Estudiante, column_name='id_estudiante',
                                 backref='calificaciones', null=True)
    # UML: una Evaluación tiene muchas Calificaciones (1 a *)
    evaluacion = ForeignKeyField(Evaluacion, column_name='id_evaluacion',
                                 backref='calificaciones', null=True)

    class Meta:
        table_name = 'calificaciones'

    @classmethod
    def columnas(cls):
        return ['Id', 'Estudiante', 'Evaluación', 'Nota', 'Situación', 'Fecha', 'Observación']

    def fila(self):
        return [self.id_calificacion,
                self.estudiante.nombre if self.estudiante else '-',
                self.evaluacion.descripcion() if self.evaluacion else '-',
                formatear_nota(self.obtener_nota()),
                'Aprobada' if self.esta_aprobada() else 'Reprobada',
                formatear_fecha(self.fechaRegistro),
                texto_o_guion(self.observacion)]

    def descripcion(self):
        return f'{formatear_nota(self.nota)} en {self.evaluacion.nombre if self.evaluacion else "-"}'

    # ----- Métodos del diagrama UML -----

    def validar_nota(self):  # UML: validarNota()
        return self.nota is not None and NOTA_MINIMA <= Decimal(str(self.nota)) <= NOTA_MAXIMA

    def obtener_nota(self):  # UML: obtenerNota()
        return self.nota

    def esta_aprobada(self):
        return self.nota is not None and Decimal(str(self.nota)) >= NOTA_APROBACION
