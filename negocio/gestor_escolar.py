from datos.models import Estudiantes, Cursos

class GestorEscolar:
    def registrar_estudiante(self, nombre, rut, fecha):
        try:
            Estudiantes.create(nombre=nombre, rut=rut, fecha_nacimiento=fecha)
            print("¡Estudiante guardado con éxito!")
        except Exception as e:
            print(f"Error al guardar estudiante: {e}")

    def obtener_estudiantes(self):
        try:
            return Estudiantes.select()
        except Exception as e:
            print(f"Error al listar: {e}")
            return []
