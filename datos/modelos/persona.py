from peewee import CharField
from datos.modelos.base import BaseModel


class Persona(BaseModel):
    """Clase padre de Estudiante, Docente y Apoderado (herencia).

    No tiene tabla propia: sus hijas heredan el atributo nombre y estos métodos.
    Cada hija redefine tipo() y mostrar_datos() (polimorfismo).
    """
    nombre = CharField(max_length=100)

    def tipo(self):
        """Nombre del rol de la persona ('Estudiante', 'Docente'...)."""
        raise NotImplementedError('Cada tipo de persona debe definir su tipo.')

    def descripcion(self):
        return self.nombre

    def mostrar_datos(self):  # UML: mostrarDatos()
        """Ficha de la persona. Las clases hijas agregan sus propios datos."""
        return f'{self.tipo()}: {self.nombre}'
