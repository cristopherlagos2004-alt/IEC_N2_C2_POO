from datos.auxiliares.validaciones import validar_nombre, validar_rut, validar_telefono
from datos.repositorio.repositorio_apoderados import RepositorioApoderados
from negocio.negocio_base import NegocioBase


class NegocioApoderados(NegocioBase):
    nombre_entidad = 'el apoderado'
    validadores = {
        'rut': validar_rut,
        'nombre': validar_nombre,
        'telefono': validar_telefono,
    }

    def __init__(self, repositorio=None):
        super().__init__(repositorio or RepositorioApoderados())

    def _verificar_reglas(self, datos, actual=None):
        if self.repositorio.existe_rut(datos['rut'], self._id(actual)):
            raise ValueError(f'Ya existe un apoderado con RUT {datos["rut"]}.')

    def ficha(self, apoderado):
        """Usa mostrar_datos() del modelo (UML: mostrarDatos())."""
        return self.repositorio.ejecutar(apoderado.mostrar_datos)
