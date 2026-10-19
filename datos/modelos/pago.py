from peewee import AutoField, IntegerField, CharField, ForeignKeyField
from datos.auxiliares.formatos import formatear_monto
from datos.modelos.base import BaseModel
from datos.modelos.apoderado import Apoderado

ESTADOS_PAGO = ('Pendiente', 'Pagado')


class Pago(BaseModel):
    id_pago = AutoField()
    monto = IntegerField()  # en pesos chilenos, sin decimales
    estado = CharField(max_length=30)
    # UML: un Apoderado tiene muchos Pagos (1 a *)
    apoderado = ForeignKeyField(Apoderado, column_name='id_apoderado',
                                backref='pagos', null=True)

    class Meta:
        table_name = 'pagos'

    @classmethod
    def columnas(cls):
        return ['Id', 'Apoderado', 'Monto', 'Estado']

    def fila(self):
        return [self.id_pago, self.apoderado.nombre if self.apoderado else '-',
                formatear_monto(self.monto), self.estado]

    def descripcion(self):
        return f'{formatear_monto(self.monto)} ({self.estado})'

    # ----- Métodos del diagrama UML -----

    def registrar_pago(self):  # UML: registrarPago()
        """Marca el pago como pagado. Lanza ValueError si ya estaba pagado."""
        if self.esta_pagado():
            raise ValueError('Este pago ya estaba registrado como pagado.')
        self.estado = 'Pagado'

    def esta_pagado(self):
        return self.estado == 'Pagado'
