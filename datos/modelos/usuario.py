from peewee import AutoField, CharField, BooleanField, DateTimeField
from auxiliares.formatos import formatear_fecha_hora
from datos.model_base import ModelBase


class Usuario(ModelBase):
    """Usuario que puede iniciar sesión en el sistema.

    Seguridad: la contraseña NO se guarda; se guarda solo su hash BCrypt (clave_hash).
    Eliminación lógica: un usuario no se borra, se deshabilita (activo = False)
    y desde ese momento ya no puede iniciar sesión.
    """
    id_usuario = AutoField()
    nombre_usuario = CharField(max_length=30, unique=True)
    nombre = CharField(max_length=100)
    clave_hash = CharField(max_length=255)
    activo = BooleanField(default=True)
    ultimo_acceso = DateTimeField(null=True)

    class Meta:
        table_name = 'usuarios'

    @classmethod
    def columnas(cls):
        # El hash de la contraseña nunca se muestra
        return ['Id', 'Usuario', 'Nombre', 'Estado', 'Último acceso']

    def fila(self):
        return [self.id_usuario, self.nombre_usuario, self.nombre, self.estado(),
                formatear_fecha_hora(self.ultimo_acceso)]

    def descripcion(self):
        return self.nombre_usuario

    def estado(self):
        return 'Activo' if self.activo else 'Deshabilitado'

    def mostrar_datos(self):
        return (f'Usuario: {self.nombre_usuario}\n'
                f'Nombre: {self.nombre}\n'
                f'Estado: {self.estado()}\n'
                f'Último acceso: {formatear_fecha_hora(self.ultimo_acceso)}')
