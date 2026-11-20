from datos.modelos import Usuario
from datos.repositorio.repositorio_base import RepositorioBase


class RepositorioUsuarios(RepositorioBase):
    modelo = Usuario

    def _condicion_busqueda(self, texto):
        return Usuario.nombre_usuario.contains(texto)

    def obtener_por_nombre(self, nombre_usuario):
        """Devuelve el usuario con ese nombre, o None si no existe.

        Peewee arma la consulta con parámetros (WHERE nombre_usuario = %s),
        así que el texto del usuario nunca se pega dentro del SQL: no hay
        inyección SQL aunque escriba algo como  ' OR '1'='1
        """
        return self.ejecutar(
            lambda: Usuario.select().where(Usuario.nombre_usuario == nombre_usuario).first())

    def existe_nombre(self, nombre_usuario):
        return self._existe(Usuario.nombre_usuario == nombre_usuario)
