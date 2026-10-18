from peewee import AutoField, IntegerField, CharField, ForeignKeyField
from datos.modelos.base import BaseModel
from datos.modelos.apoderado import Apoderado


class Pago(BaseModel):
    id_pago = AutoField()
    monto = IntegerField()  # en pesos chilenos, sin decimales
    estado = CharField(max_length=30)
    # UML: un Apoderado tiene muchos Pagos (1 a *)
    apoderado = ForeignKeyField(Apoderado, column_name='id_apoderado',
                                backref='pagos', null=True)

    class Meta:
        table_name = 'pagos'
