from datos.modelos import Pago, Apoderado
from datos.repositorio.repositorio_base import RepositorioBase


class RepositorioPagos(RepositorioBase):
    modelo = Pago

    def buscar(self, texto):
        # Polimorfismo: los pagos se buscan por el nombre del apoderado
        return self.ejecutar(lambda: list(
            Pago.select().join(Apoderado)
            .where(Apoderado.nombre.contains(texto))
            .order_by(Pago.id_pago)))
