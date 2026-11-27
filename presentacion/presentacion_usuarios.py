from auxiliares.mensajes import CLAVES_NO_COINCIDEN
from presentacion.consola import pedir_clave
from presentacion.menu_crud import MenuCrud


class MenuUsuarios(MenuCrud):
    """CRUD de usuarios: listar, registrar, buscar, actualizar y deshabilitar.

    Las contraseñas se piden con maskpass (no se ven en pantalla) y nunca se muestran.
    """

    def __init__(self, negocio):
        super().__init__('Usuarios', negocio)

    @property
    def texto_busqueda(self):
        return 'el usuario o nombre'

    @property
    def texto_eliminar(self):
        # Polimorfismo: los usuarios no se borran, se deshabilitan
        return 'Deshabilitar'

    def pedir_datos(self, actual=None):
        datos = {
            'nombre_usuario': self._pedir('nombre_usuario', 'Nombre de usuario (ej: cristopher.lagos)',
                                          actual),
            'nombre': self._pedir('nombre', 'Nombre completo', actual),
        }
        if actual is None:
            # Solo al registrar se pide la contraseña; para cambiarla hay una opción aparte
            datos['clave'] = self._pedir_clave_nueva()
        return datos

    def _pedir_clave_nueva(self):
        """Pide la contraseña dos veces y la valida al tiro."""
        print('La contraseña debe tener al menos 8 caracteres, con letras y números.')
        while True:
            clave = pedir_clave('Contraseña')
            try:
                self.negocio.validar_campo('clave', clave)
            except ValueError as error:
                print(f'  >> {error} Intente nuevamente.')
                continue
            if pedir_clave('Repita la contraseña') == clave:
                return clave
            print(f'  >> {CLAVES_NO_COINCIDEN} Intente nuevamente.')

    def opciones_extra(self):
        return [
            ('Cambiar contraseña', self.cambiar_clave),
            ('Habilitar usuario', self.habilitar),
        ]

    def cambiar_clave(self):
        usuario = self.seleccionar('cambiar su contraseña')
        if usuario is None:
            return
        clave_actual = None
        if self.negocio.es_usuario_sesion(usuario):
            clave_actual = pedir_clave('Contraseña actual')
        nueva = pedir_clave('Contraseña nueva (mín. 8 caracteres, con letras y números)')
        confirmacion = pedir_clave('Repita la contraseña nueva')
        _, mensaje = self.negocio.cambiar_clave(usuario, nueva, confirmacion, clave_actual)
        print(mensaje)

    def habilitar(self):
        usuario = self.seleccionar('habilitar')
        if usuario is None:
            return
        _, mensaje = self.negocio.habilitar(usuario)
        print(mensaje)
