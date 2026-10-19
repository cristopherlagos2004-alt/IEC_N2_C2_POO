from datos.modelos import Calificacion, Estudiante
from datos.repositorio.repositorio_base import RepositorioBase


class RepositorioCalificaciones(RepositorioBase):
    modelo = Calificacion

    def buscar(self, texto):
        # Polimorfismo: las calificaciones se buscan por el nombre del estudiante
        return self.ejecutar(lambda: list(
            Calificacion.select().join(Estudiante)
            .where(Estudiante.nombre.contains(texto))
            .order_by(Calificacion.id_calificacion)))

    def existe_calificacion(self, estudiante, evaluacion, excluir_id=None):
        """Un estudiante tiene una sola nota por evaluación."""
        return self._existe((Calificacion.estudiante == estudiante) &
                            (Calificacion.evaluacion == evaluacion), excluir_id)
