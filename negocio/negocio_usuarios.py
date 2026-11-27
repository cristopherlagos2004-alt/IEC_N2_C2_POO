from datetime import datetime

from auxiliares.mensajes import LOGIN_INCORRECTO, LOGIN_BIENVENIDA, CLAVES_NO_COINCIDEN
from auxiliares.seguridad import generar_hash, verificar_clave
from auxiliares.validaciones import validar_nombre_usuario, validar_nombre, validar_clave
from datos.repositorio import repositorio_usuarios
from negocio.negocio_base import NegocioBase


class NegocioUsuarios(NegocioBase):
    """Reglas de los usuarios del sistema y del inicio de sesión (login).

    Encapsulamiento: el usuario que inició sesión es un atributo privado
    (__usuario_sesion) que solo se puede leer con la propiedad usuario_sesion;
    solo cambia a través de iniciar_sesion() y cerrar_sesion().
    """
    nombre_entidad = 'el usuario'
    validadores = {
        'nombre_usuario': validar_nombre_usuario,
        'nombre': validar_nombre,
        'clave': validar_clave,
    }

    def __init__(self, repositorio=None):
        super().__init__(repositorio or repositorio_usuarios)
        self.__usuario_sesion = None

    @property
    def usuario_sesion(self):
        """Usuario que inició sesión (None si nadie ha iniciado sesión)."""
        return self.__usuario_sesion

    # ----- Login -----

    def hay_usuarios_activos(self):
        return self.repositorio.contar_activos() > 0

    def iniciar_sesion(self, nombre_usuario, clave):
        """Revisa las credenciales. Devuelve (exito, mensaje).

        El mensaje de error es el mismo si el usuario no existe o si la contraseña
        está mala, para no darle pistas a un atacante.
        """
        nombre_usuario = str(nombre_usuario).strip().lower()
        usuario = self.repositorio.buscar_por_nombre_usuario(nombre_usuario) if nombre_usuario else None
        # Se verifica aunque el usuario no exista (con hash None), para que tarde lo mismo
        if not verificar_clave(clave, usuario.clave_hash if usuario else None):
            return False, LOGIN_INCORRECTO
        usuario.ultimo_acceso = datetime.now().replace(microsecond=0)
        self.repositorio.guardar(usuario)
        self.__usuario_sesion = usuario
        return True, LOGIN_BIENVENIDA.format(nombre=usuario.nombre)

    def cerrar_sesion(self):
        self.__usuario_sesion = None

    def es_usuario_sesion(self, usuario):
        return (self.__usuario_sesion is not None
                and usuario.get_id() == self.__usuario_sesion.get_id())

    # ----- CRUD -----

    def _validar(self, datos):
        """Polimorfismo: además de validar, reemplaza la contraseña por su hash BCrypt.
        Así la contraseña en texto plano nunca llega a la base de datos."""
        limpios = super()._validar(datos)
        if 'clave' in limpios:
            limpios['clave_hash'] = generar_hash(limpios.pop('clave'))
        return limpios

    def _verificar_reglas(self, datos, actual=None):
        if self.repositorio.existe_nombre_usuario(datos['nombre_usuario'], self._id(actual)):
            raise ValueError(f'Ya existe el usuario "{datos["nombre_usuario"]}" '
                             '(puede estar deshabilitado).')

    def eliminar(self, registro):
        """Polimorfismo: los usuarios no se borran, se deshabilitan (eliminación lógica)."""
        if self.es_usuario_sesion(registro):
            return False, 'No puede deshabilitar su propio usuario mientras tiene la sesión iniciada.'
        if not registro.activo:
            return False, f'El usuario "{registro.descripcion()}" ya está deshabilitado.'
        self.repositorio.eliminar(registro)
        return True, f'Se deshabilitó {self._nombrar(registro)}. Ya no podrá iniciar sesión.'

    def habilitar(self, registro):
        if registro.activo:
            return False, f'El usuario "{registro.descripcion()}" ya está activo.'
        self.repositorio.habilitar(registro)
        return True, f'Se habilitó {self._nombrar(registro)}.'

    def cambiar_clave(self, registro, clave_nueva, confirmacion, clave_actual=None):
        """Cambia la contraseña. Devuelve (exito, mensaje).

        Si el usuario cambia SU PROPIA contraseña, debe escribir la actual
        (por si alguien usa el computador mientras la sesión está abierta).
        """
        if self.es_usuario_sesion(registro) and not verificar_clave(clave_actual or '',
                                                                     registro.clave_hash):
            return False, 'La contraseña actual no es correcta.'
        try:
            clave_nueva = self.validar_campo('clave', clave_nueva)
        except ValueError as error:
            return False, str(error)
        if clave_nueva != confirmacion:
            return False, CLAVES_NO_COINCIDEN
        registro.clave_hash = generar_hash(clave_nueva)
        self.repositorio.guardar(registro)
        return True, f'Se cambió la contraseña del usuario "{registro.descripcion()}".'
