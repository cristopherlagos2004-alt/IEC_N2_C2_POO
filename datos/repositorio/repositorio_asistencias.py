from datos.modelos import Asistencia, Estudiante
from datos.repositorio.repositorio_base import RepositorioBase


class RepositorioAsistencias(RepositorioBase):
    modelo = Asistencia

    def buscar(self, texto):
        # Polimorfismo: las asistencias se buscan por el nombre del estudiante
        return self.ejecutar(lambda: list(
            Asistencia.select().join(Estudiante)
            .where(Estudiante.nombre.contains(texto))
            .order_by(Asistencia.fecha, Asistencia.id_asistencia)))

    def existe_asistencia(self, estudiante, fecha, excluir_id=None):
        """Un estudiante tiene un solo registro de asistencia por día."""
        return self._existe((Asistencia.estudiante == estudiante) &
                            (Asistencia.fecha == fecha), excluir_id)
