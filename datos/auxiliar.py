import logging

nombre_app = 'Sistema de Gestión Escolar - INACAP'
version_app = 'v1.1'

main_menu = {
    '1': 'Listar Estudiantes',
    '2': 'Registrar Estudiante',
    '3': 'Buscar Estudiante por Nombre',
    '4': 'Actualizar Estudiante',
    '5': 'Eliminar (desactivar) Estudiante',
    '6': 'Salir'
}

mensaje_error_orm = 'Ocurrió un error con la base de datos. Revise el archivo errores.log.'

# El detalle técnico de los errores se guarda en un archivo y no se muestra
# en pantalla, para no exponer información interna de la base de datos.
# delay=True: el archivo solo se crea cuando ocurre el primer error.
_manejador = logging.FileHandler('errores.log', encoding='utf-8', delay=True)
_manejador.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
logger = logging.getLogger('gestion_escolar')
logger.setLevel(logging.ERROR)
logger.addHandler(_manejador)


def registrar_error(error):
    logger.error('Error de base de datos: %s', error, exc_info=error)
    print(mensaje_error_orm)
