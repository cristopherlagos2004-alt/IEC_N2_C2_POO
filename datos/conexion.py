from decouple import config
from peewee import MySQLDatabase

# Los datos de conexión se leen SIEMPRE desde el archivo .env (ver .env.example).
# DB_USER y DB_PASSWORD no tienen valor por defecto a propósito:
# si faltan, el programa avisa en vez de conectarse como root sin contraseña.
base_datos = MySQLDatabase(
    config('DB_NAME', default='gestion_escolar'),
    host=config('DB_HOST', default='localhost'),
    port=config('DB_PORT', default=3306, cast=int),
    user=config('DB_USER'),
    password=config('DB_PASSWORD'),
    charset='utf8mb4',
)
