from peewee import AutoField, CharField
from datos.auxiliares.formatos import texto_o_guion
from datos.modelos.persona import Persona


class Docente(Persona):
    """Hereda de Persona el atributo nombre y el método mostrar_datos()."""
    id_docente = AutoField()
    correo = CharField(max_length=100, null=True)
    especialidad = CharField(max_length=100, null=True)

    class Meta:
        table_name = 'docentes'

    @classmethod
    def columnas(cls):
        return ['Id', 'Nombre', 'Correo', 'Especialidad']

    def fila(self):
        return [self.id_docente, self.nombre, texto_o_guion(self.correo),
                texto_o_guion(self.especialidad)]

    def tipo(self):
        return 'Docente'

    def mostrar_datos(self):
        # Polimorfismo: usa la versión de Persona y le agrega datos propios
        return (f'{super().mostrar_datos()}\n'
                f'Correo: {texto_o_guion(self.correo)}\n'
                f'Especialidad: {texto_o_guion(self.especialidad)}')

    # ----- Métodos del diagrama UML -----

    def consultar_asignaturas(self):  # UML: impartirAsignatura()
        """Asignaturas que imparte el docente."""
        return sorted(self.asignaturas, key=lambda a: a.nombre)

    def consultar_estudiantes(self):  # UML: consultarEstudiantes()
        """Estudiantes de los cursos donde el docente hace clases."""
        cursos = {a.curso for a in self.asignaturas if a.curso is not None}
        estudiantes = [e for curso in cursos for e in curso.listar_estudiantes()]
        return sorted(estudiantes, key=lambda e: e.nombre)
