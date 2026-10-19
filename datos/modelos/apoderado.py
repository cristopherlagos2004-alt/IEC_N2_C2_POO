from peewee import AutoField, CharField
from datos.auxiliares.formatos import texto_o_guion
from datos.modelos.persona import Persona


class Apoderado(Persona):
    """Hereda de Persona el atributo nombre y el método mostrar_datos().

    UML: un Apoderado tiene muchos Estudiantes y muchos Pagos (1 a *).
    Esas relaciones están en los modelos Estudiante y Pago.
    """
    id_apoderado = AutoField()
    rut = CharField(max_length=15, unique=True)
    telefono = CharField(max_length=20, null=True)

    class Meta:
        table_name = 'apoderados'

    @classmethod
    def columnas(cls):
        return ['Id', 'RUT', 'Nombre', 'Teléfono', 'Estudiantes a cargo']

    def fila(self):
        return [self.id_apoderado, self.rut, self.nombre, texto_o_guion(self.telefono),
                len(self.estudiantes_a_cargo())]

    def tipo(self):
        return 'Apoderado'

    def mostrar_datos(self):  # UML: mostrarDatos()
        a_cargo = ', '.join(e.nombre for e in self.estudiantes_a_cargo()) or '-'
        return (f'{super().mostrar_datos()}\n'
                f'RUT: {self.rut}\n'
                f'Teléfono: {texto_o_guion(self.telefono)}\n'
                f'Estudiantes a cargo: {a_cargo}')

    def estudiantes_a_cargo(self):
        return sorted((e for e in self.estudiantes if e.activo), key=lambda e: e.nombre)
