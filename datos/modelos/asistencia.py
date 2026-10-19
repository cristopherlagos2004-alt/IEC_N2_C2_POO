from peewee import AutoField, DateField, BooleanField, CharField, ForeignKeyField
from datos.auxiliares.formatos import formatear_fecha, texto_o_guion
from datos.modelos.base import BaseModel
from datos.modelos.estudiante import Estudiante


class Asistencia(BaseModel):
    id_asistencia = AutoField()
    fecha = DateField()
    presente = BooleanField(default=True)
    observacion = CharField(max_length=500, null=True)
    # UML: un Estudiante tiene muchas Asistencias (1 a *)
    estudiante = ForeignKeyField(Estudiante, column_name='id_estudiante',
                                 backref='asistencias', null=True)

    class Meta:
        table_name = 'asistencias'

    @classmethod
    def columnas(cls):
        return ['Id', 'Fecha', 'Estudiante', 'Estado', 'Observación']

    def fila(self):
        return [self.id_asistencia, formatear_fecha(self.fecha),
                self.estudiante.nombre if self.estudiante else '-',
                self.texto_estado(), texto_o_guion(self.observacion)]

    def descripcion(self):
        nombre = self.estudiante.nombre if self.estudiante else '-'
        return f'{formatear_fecha(self.fecha)} - {nombre}: {self.texto_estado()}'

    # ----- Métodos del diagrama UML -----

    def consultar_estado(self):  # UML: consultarEstado()
        """True si el estudiante estuvo presente."""
        return bool(self.presente)

    def texto_estado(self):
        return 'Presente' if self.consultar_estado() else 'Ausente'
