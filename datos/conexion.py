from decouple import config
from peewee import MySQLDatabase

def conectar_db():
    conexion = MySQLDatabase(config('db', default='gestion_escolar'), **{
        'charset': 'utf8mb4',
        'host': config('host', default='localhost'),
        'port': config('port', default=3306, cast=int),
        'user': config('user', default='root'),
        'password': config('password', default='')})
    return conexion
