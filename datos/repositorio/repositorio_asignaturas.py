from datos.modelos import Asignatura
from datos.repositorio.repositorio_base import RepositorioBase


class RepositorioAsignaturas(RepositorioBase):
    modelo = Asignatura

    def _condicion_busqueda(self, texto):
        # Polimorfismo: las asignaturas se buscan por nombre o por código
        return Asignatura.nombre.contains(texto) | Asignatura.codigo.contains(texto)

    def existe_codigo(self, codigo, curso, excluir_id=None):
        """True si ya hay una asignatura con ese código en el mismo curso."""
        return self._existe((Asignatura.codigo == codigo) & (Asignatura.curso == curso), excluir_id)
