from datos.auxiliares.formatos import formatear_nota, formatear_porcentaje
from datos.auxiliares.validaciones import validar_rut, validar_nombre, validar_fecha_nacimiento
from datos.repositorio.repositorio_estudiantes import RepositorioEstudiantes
from negocio.negocio_base import NegocioBase


class NegocioEstudiantes(NegocioBase):
    nombre_entidad = 'el estudiante'
    validadores = {
        'rut': validar_rut,
        'nombre': validar_nombre,
        'fecha_nacimiento': validar_fecha_nacimiento,
    }

    def __init__(self, repositorio=None):
        super().__init__(repositorio or RepositorioEstudiantes())

    def _verificar_reglas(self, datos, actual=None):
        if self.repositorio.existe_rut(datos['rut'], self._id(actual)):
            raise ValueError(f'Ya existe un estudiante con RUT {datos["rut"]} '
                             '(puede estar desactivado).')

    def eliminar(self, registro):
        # Polimorfismo: redefine eliminar(). No revisa dependencias porque el
        # repositorio de estudiantes hace eliminación lógica (no borra la fila).
        nombre = self._nombrar(registro)
        self.repositorio.eliminar(registro)
        return True, f'Se desactivó {nombre}. Sus notas y asistencias se conservan.'

    def ficha(self, estudiante):
        """Ficha académica: usa los métodos del modelo que vienen del UML."""
        return self.repositorio.ejecutar(lambda: {
            'datos': estudiante.mostrar_datos(),
            'promedio': formatear_nota(estudiante.obtener_promedio()),
            'asistencia': formatear_porcentaje(estudiante.obtener_porcentaje_asistencia()),
            'notas': estudiante.consultar_notas(),
            'asignaturas': estudiante.consultar_asignaturas(),
        })
