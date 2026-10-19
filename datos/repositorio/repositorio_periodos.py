from datos.modelos import PeriodoAcademico
from datos.repositorio.repositorio_base import RepositorioBase


class RepositorioPeriodos(RepositorioBase):
    modelo = PeriodoAcademico

    def _condicion_busqueda(self, texto):
        # Polimorfismo: los periodos no tienen nombre; se buscan por año o por estado
        if texto.isdigit():
            return PeriodoAcademico.anio == int(texto)
        return PeriodoAcademico.estado.contains(texto)

    def existe_periodo(self, anio, semestre, excluir_id=None):
        return self._existe((PeriodoAcademico.anio == anio) &
                            (PeriodoAcademico.semestre == semestre), excluir_id)

    def existe_otro_activo(self, excluir_id=None):
        return self._existe(PeriodoAcademico.estado == 'Activo', excluir_id)
