from datos.modelos import Curso
from datos.repositorio.repositorio_base import RepositorioBase


class RepositorioCursos(RepositorioBase):
    modelo = Curso

    def existe_nombre(self, nombre, periodo, excluir_id=None):
        """True si ya hay un curso con ese nombre en el mismo periodo."""
        return self._existe((Curso.nombre == nombre) & (Curso.periodo == periodo), excluir_id)
