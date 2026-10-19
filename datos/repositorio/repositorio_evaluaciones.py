from peewee import fn
from datos.modelos import Evaluacion
from datos.repositorio.repositorio_base import RepositorioBase


class RepositorioEvaluaciones(RepositorioBase):
    modelo = Evaluacion

    def suma_porcentajes(self, asignatura, excluir_id=None):
        """Suma de las ponderaciones de las evaluaciones de una asignatura."""
        consulta = (Evaluacion.select(fn.COALESCE(fn.SUM(Evaluacion.porcentaje), 0))
                    .where(Evaluacion.asignatura == asignatura))
        if excluir_id is not None:
            consulta = consulta.where(Evaluacion.id_evaluacion != excluir_id)
        return self.ejecutar(consulta.scalar)
