from datetime import datetime

from peewee import AutoField, CharField, IntegerField, DateTimeField
from datos.modelos.base import BaseModel


class Usuario(BaseModel):
    """Usuario que puede iniciar sesión (Evaluación 3).

    Guarda el hash de la contraseña, nunca la contraseña.
    columnas() y fila() no incluyen el hash, para que no se muestre por error
    si alguien lista los usuarios en una tabla.
    """
    id_usuario = AutoField()
    nombre_usuario = CharField(max_length=30, unique=True)
    hash_contrasena = CharField(max_length=255)
    intentos_fallidos = IntegerField(default=0)
    bloqueado_hasta = DateTimeField(null=True)

    class Meta:
        table_name = 'usuarios'

    @classmethod
    def columnas(cls):
        return ['Id', 'Usuario', 'Bloqueado']

    def fila(self):
        return [self.id_usuario, self.nombre_usuario, 'Sí' if self.esta_bloqueado() else 'No']

    def descripcion(self):
        return self.nombre_usuario

    def esta_bloqueado(self, ahora=None):
        ahora = ahora or datetime.now()
        return self.bloqueado_hasta is not None and self.bloqueado_hasta > ahora
