from datos.modelos import Apoderado
from datos.repositorio.repositorio_base import RepositorioBase


class RepositorioApoderados(RepositorioBase):
    modelo = Apoderado

    def existe_rut(self, rut, excluir_id=None):
        return self._existe(Apoderado.rut == rut, excluir_id)
