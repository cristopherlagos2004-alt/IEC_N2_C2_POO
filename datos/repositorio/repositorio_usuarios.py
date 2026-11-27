"""Repositorio de usuarios: funciones para guardar y consultar la tabla usuarios."""
from datos.modelos import Usuario
from datos.repositorio import repositorio_base as base
from datos.repositorio.repositorio_base import ejecutar  # noqa: F401  (la capa de negocio también la usa)

# Modelo que maneja este repositorio (la capa de negocio lo usa para crear registros)
modelo = Usuario


def guardar(usuario):
    """Inserta el usuario si es nuevo, o lo actualiza si ya existe, usando save()."""
    ejecutar(lambda: usuario.save())


def listar():
    """Todos los usuarios (activos y deshabilitados), ordenados por Id.
    Se muestran también los deshabilitados para poder volver a habilitarlos."""
    return base.listar(Usuario)


def obtener_por_id(id_usuario):
    """El usuario con ese Id, o None si no existe."""
    return base.obtener_por_id(Usuario, id_usuario)


def buscar(texto):
    """Usuarios cuyo nombre de usuario o nombre contiene el texto."""
    return base.buscar(Usuario, Usuario.nombre_usuario.contains(texto) |
                       Usuario.nombre.contains(texto))


def buscar_por_nombre_usuario(nombre_usuario):
    """El usuario ACTIVO con ese nombre de usuario (exacto), o None. Se usa en el login."""
    return ejecutar(lambda: Usuario.get_or_none(
        (Usuario.nombre_usuario == nombre_usuario) & (Usuario.activo == True)))  # noqa: E712


def eliminar(usuario):
    """Eliminación LÓGICA: el usuario no se borra, se deshabilita (ya no puede entrar)."""
    base.deshabilitar(usuario)


def habilitar(usuario):
    usuario.activo = True
    guardar(usuario)


def contar_dependencias(usuario):
    return base.contar_dependencias(Usuario, usuario)


def existe_nombre_usuario(nombre_usuario, excluir_id=None):
    """Revisa TODOS los usuarios, incluso los deshabilitados (el nombre de usuario es único)."""
    return base.existe(Usuario, Usuario.nombre_usuario == nombre_usuario, excluir_id)


def contar_activos():
    return ejecutar(Usuario.select().where(Usuario.activo == True).count)  # noqa: E712
