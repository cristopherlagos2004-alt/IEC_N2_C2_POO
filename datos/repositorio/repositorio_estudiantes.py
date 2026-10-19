from datos.modelos import Estudiante
from datos.repositorio.repositorio_base import RepositorioBase


class RepositorioEstudiantes(RepositorioBase):
    modelo = Estudiante

    def _consulta_base(self):
        # Polimorfismo: solo se muestran los estudiantes activos
        return Estudiante.select().where(Estudiante.activo == True)  # noqa: E712

    def eliminar(self, registro):
        """Polimorfismo: redefine eliminar() con una eliminación LÓGICA.
        No borra la fila (se conservan sus notas y asistencias): la marca como inactiva."""
        registro.activo = False
        self.guardar(registro)

    def existe_rut(self, rut, excluir_id=None):
        """Revisa TODOS los estudiantes, incluso los desactivados (el RUT es único)."""
        return self._existe(Estudiante.rut == rut, excluir_id)
