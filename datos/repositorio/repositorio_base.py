"""Funciones comunes que usan todos los repositorios.

La pauta pide repositorios hechos con FUNCIONES (no con clases). Para no repetir
el mismo código en cada repositorio, aquí están las funciones genéricas: reciben
el modelo con el que trabajan. Cada repositorio (repositorio_docentes.py, etc.)
las usa para armar sus propias funciones: guardar, listar, buscar, eliminar...
"""
from peewee import PeeweeException, IntegrityError
from auxiliares.errores import ErrorDatos, registrar_error
from auxiliares.mensajes import MENSAJE_GENERAL, MENSAJE_INTEGRIDAD


# ----- Manejo de errores -----

def ejecutar(operacion):
    """Ejecuta una operación de base de datos.

    Si falla, guarda el detalle en errores.log y lanza ErrorDatos
    con un mensaje que se puede mostrar al usuario.
    """
    try:
        return operacion()
    except IntegrityError as error:
        registrar_error(error)
        raise ErrorDatos(MENSAJE_INTEGRIDAD) from error
    except PeeweeException as error:
        registrar_error(error)
        raise ErrorDatos(MENSAJE_GENERAL) from error


# ----- Escritura -----

def guardar(registro):
    """Inserta (si es nuevo) o actualiza (si ya existe) el registro con save()."""
    ejecutar(lambda: registro.save())


def eliminar(registro):
    """Eliminación física: borra la fila de la tabla."""
    ejecutar(lambda: registro.delete_instance())


def deshabilitar(registro):
    """Eliminación lógica: no borra la fila, la marca como inactiva (campo activo)."""
    registro.activo = False
    guardar(registro)


# ----- Consultas -----

def listar(modelo, consulta=None):
    """Todos los registros, ordenados por su Id.
    'consulta' permite partir de un filtro (ej: solo estudiantes activos)."""
    consulta = consulta if consulta is not None else modelo.select()
    return ejecutar(lambda: list(consulta.order_by(modelo._meta.primary_key)))


def obtener_por_id(modelo, id_registro, consulta=None):
    """El registro con ese Id, o None si no existe."""
    consulta = consulta if consulta is not None else modelo.select()
    return ejecutar(lambda: consulta.where(modelo._meta.primary_key == id_registro).first())


def buscar(modelo, condicion, consulta=None):
    """Registros que cumplen la condición de búsqueda."""
    consulta = consulta if consulta is not None else modelo.select()
    return ejecutar(lambda: list(consulta.where(condicion)
                                 .order_by(modelo._meta.primary_key)))


def existe(modelo, condicion, excluir_id=None):
    """True si hay algún registro que cumple la condición (sin contar excluir_id).
    Sirve para revisar datos repetidos, como un RUT o un nombre de usuario."""
    consulta = modelo.select().where(condicion)
    if excluir_id is not None:
        consulta = consulta.where(modelo._meta.primary_key != excluir_id)
    return ejecutar(consulta.exists)


def contar_dependencias(modelo, registro):
    """Registros de otras tablas que apuntan a este (ej: asignaturas de un docente).

    Devuelve una lista de (nombre de la tabla, cantidad), solo con las que tienen alguno.
    Sirve para avisar antes de eliminar, en vez de que la base de datos lo rechace.
    """
    def contar():
        resultado = []
        # _meta.backrefs: relaciones de otros modelos que apuntan a este
        for campo, modelo_dependiente in modelo._meta.backrefs.items():
            cantidad = modelo_dependiente.select().where(campo == registro).count()
            if cantidad:
                resultado.append((modelo_dependiente._meta.table_name, cantidad))
        return resultado
    return ejecutar(contar)
