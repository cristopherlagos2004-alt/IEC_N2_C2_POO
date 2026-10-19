from decouple import config, UndefinedValueError
from peewee import MySQLDatabase, OperationalError

# Objeto de base de datos que comparten todos los modelos.
# Se crea "vacío" (None) y la clase Conexion lo configura con los datos del .env.
base_datos = MySQLDatabase(None)


class Conexion:
    """Maneja la conexión a MySQL.

    Encapsulamiento: el objeto de base de datos es un atributo privado (__base_datos)
    y desde afuera solo se puede leer con la propiedad base_datos.
    """

    def __init__(self, base=base_datos):
        self.__base_datos = base

    @property
    def base_datos(self):
        return self.__base_datos

    def conectar(self):
        """Lee el archivo .env y abre la conexión. Devuelve (exito, mensaje)."""
        try:
            self.__base_datos.init(
                config('DB_NAME', default='gestion_escolar'),
                host=config('DB_HOST', default='localhost'),
                port=config('DB_PORT', default=3306, cast=int),
                # DB_USER y DB_PASSWORD no tienen valor por defecto a propósito:
                # si faltan, avisamos en vez de conectarnos como root sin contraseña.
                user=config('DB_USER'),
                password=config('DB_PASSWORD'),
                charset='utf8mb4',
            )
        except UndefinedValueError:
            return False, 'Falta configurar el archivo .env (copie .env.example y complete sus datos).'

        try:
            self.__base_datos.connect(reuse_if_open=True)
        except OperationalError:
            return False, ('No se pudo conectar a la base de datos. '
                           'Revise el archivo .env y que MySQL esté encendido.')
        return True, 'Conexión establecida.'

    def desconectar(self):
        if self.esta_conectada():
            self.__base_datos.close()

    def esta_conectada(self):
        return not self.__base_datos.is_closed()
