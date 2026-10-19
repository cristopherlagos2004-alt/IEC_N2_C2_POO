from peewee import AutoField, IntegerField, CharField
from datos.modelos.base import BaseModel

ESTADOS_PERIODO = ('Activo', 'Cerrado', 'Inactivo')


class PeriodoAcademico(BaseModel):
    id_periodo = AutoField()
    anio = IntegerField()
    semestre = IntegerField()
    estado = CharField(max_length=30)

    class Meta:
        table_name = 'periodos_academicos'

    @classmethod
    def columnas(cls):
        return ['Id', 'Año', 'Semestre', 'Estado']

    def fila(self):
        return [self.id_periodo, self.anio, self.semestre, self.estado]

    def descripcion(self):
        return f'{self.anio}-{self.semestre} ({self.estado})'

    # ----- Métodos del diagrama UML -----

    def iniciar_periodo(self):  # UML: iniciarPeriodo()
        self.estado = 'Activo'

    def cerrar_periodo(self):  # UML: cerrarPeriodo()
        self.estado = 'Cerrado'

    def consultar_estado(self):  # UML: consultarEstado()
        return self.estado

    def cambiar_estado(self, nuevo_estado):  # UML: cambiarEstado()
        if nuevo_estado not in ESTADOS_PERIODO:
            raise ValueError(f'El estado debe ser uno de: {", ".join(ESTADOS_PERIODO)}.')
        if nuevo_estado == 'Activo':
            self.iniciar_periodo()
        elif nuevo_estado == 'Cerrado':
            self.cerrar_periodo()
        else:
            self.estado = nuevo_estado
