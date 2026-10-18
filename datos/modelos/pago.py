from datos.conexion import base_datos
from peewee import Model, AutoField, FloatField, CharField, ForeignKeyField
from datos.modelos.apoderado import Apoderado

database = base_datos()

class BaseModel(Model):
    class Meta:
        database = database

class Pago(BaseModel):
    id_pago = AutoField()
    monto = FloatField()
    estado = CharField(max_length=30)
    apoderado = ForeignKeyField(Apoderado, backref='pagos', null=True)

    class Meta:
        table_name = 'pagos'
