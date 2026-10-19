from datos.auxiliares.formatos import formatear_nota
from datos.auxiliares.validaciones import validar_texto, validar_entero, validar_codigo
from datos.repositorio.repositorio_asignaturas import RepositorioAsignaturas
from negocio.negocio_base import NegocioBase


class NegocioAsignaturas(NegocioBase):
    nombre_entidad = 'la asignatura'
    validadores = {
        'nombre': lambda texto: validar_texto(texto, 'El nombre', 50),
        'codigo': validar_codigo,
        'horasSemanales': lambda texto: validar_entero(texto, 'El número de horas semanales', 1, 45),
    }

    def __init__(self, repositorio=None):
        super().__init__(repositorio or RepositorioAsignaturas())

    def _verificar_reglas(self, datos, actual=None):
        if self.repositorio.existe_codigo(datos['codigo'], datos['curso'], self._id(actual)):
            raise ValueError(f'Ya existe una asignatura con código {datos["codigo"]} en ese curso.')

    def resumen(self, asignatura):
        """Promedio y estudiantes de la asignatura."""
        return self.repositorio.ejecutar(lambda: {
            'promedio': formatear_nota(asignatura.calcular_promedio()),
            'estudiantes': asignatura.listar_estudiantes(),
            'evaluaciones': list(asignatura.evaluaciones),
        })
