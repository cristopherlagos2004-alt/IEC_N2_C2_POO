"""Menú "Usuarios": listar, registrar, buscar, actualizar y eliminar (Evaluación 3).

Igual que los demás menús, hereda de MenuCrud y solo pide datos y muestra
resultados. Las reglas (hash, nombre repetido, no eliminar al usuario de la
sesión ni al último) están en negocio.negocio_usuarios.NegocioUsuarios.
El hash nunca se muestra: la tabla usa Usuario.columnas()/fila(), que no lo incluyen.
"""
from presentacion.consola import confirmar, pedir_contrasena_nueva
from presentacion.menu_crud import MenuCrud

REGLAS_CONTRASENA = ('La contraseña debe tener al menos 8 caracteres y como máximo 72 bytes '
                     '(la ñ y las tildes cuentan doble), con letras y números, '
                     'y no puede contener el nombre de usuario.')


class MenuUsuarios(MenuCrud):
    def __init__(self, negocio):
        super().__init__('Usuarios', negocio)

    @property
    def texto_busqueda(self):
        return 'el nombre de usuario'

    def pedir_datos(self, actual=None):
        nombre = self._pedir_nombre(actual)
        datos = {'nombre_usuario': nombre}
        # Al registrar, la contraseña es obligatoria; al actualizar, solo si se quiere cambiar
        if actual is None or confirmar('¿Desea cambiar la contraseña?'):
            print(REGLAS_CONTRASENA)
            datos['contrasena'] = pedir_contrasena_nueva(
                lambda contrasena: self.negocio.validar_contrasena(contrasena, nombre))
        return datos

    def _pedir_nombre(self, actual):
        """Como _pedir() de MenuCrud, pero además avisa al tiro si el nombre ya existe."""
        while True:
            nombre = self._pedir('nombre_usuario', 'Nombre de usuario', actual)
            try:
                self.negocio.verificar_nombre_disponible(nombre, actual)
                return nombre
            except ValueError as error:
                print(f'  >> {error} Intente nuevamente.')
