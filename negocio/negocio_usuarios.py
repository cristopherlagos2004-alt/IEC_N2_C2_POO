"""Gestión de usuarios del sistema (Evaluación 3).

Sigue el mismo patrón que las otras 10 entidades (hereda de NegocioBase), con
reglas propias:
- la contraseña nunca se guarda: se convierte en hash bcrypt antes de guardar
- no se repiten nombres de usuario
- no se puede eliminar al usuario que tiene la sesión iniciada
- no se puede dejar el sistema sin usuarios
- todas las operaciones exigen una sesión iniciada (Sesion.exigir())
"""
from datos.auxiliares.seguridad import generar_hash
from datos.auxiliares.validaciones import validar_nombre_usuario, validar_contrasena_nueva
from datos.repositorio.repositorio_usuarios import RepositorioUsuarios
from negocio.negocio_base import NegocioBase

CAMPO_CONTRASENA = 'contrasena'


class NegocioUsuarios(NegocioBase):
    nombre_entidad = 'el usuario'
    # La contraseña NO está aquí: se valida aparte porque necesita el nombre de
    # usuario (no puede contenerlo) y porque al actualizar es opcional.
    validadores = {
        'nombre_usuario': validar_nombre_usuario,
    }

    def __init__(self, sesion, repositorio=None):
        super().__init__(repositorio or RepositorioUsuarios())
        self.__sesion = sesion  # encapsulamiento: solo se usa dentro de esta clase

    # ----- Contraseña -----

    @staticmethod
    def validar_contrasena(texto, nombre_usuario=''):
        """La presentación la usa para avisar al tiro si la contraseña no sirve."""
        return validar_contrasena_nueva(texto, nombre_usuario)

    def verificar_nombre_disponible(self, texto, actual=None):
        """Avisa al tiro si el nombre ya está ocupado (antes de pedir la contraseña)."""
        nombre = validar_nombre_usuario(texto)
        if self.repositorio.existe_nombre(nombre, self._id(actual)):
            raise ValueError(f'Ya existe el usuario "{nombre}".')
        return nombre

    def _validar(self, datos):
        """Valida como NegocioBase y además cambia la contraseña por su hash.

        datos['contrasena']:
        - al registrar es obligatoria
        - al actualizar puede ser None, que significa "no cambiar la contraseña"
        Lo que se devuelve ya NO tiene la contraseña, solo 'hash_contrasena'.
        """
        datos = dict(datos)
        contrasena = datos.pop(CAMPO_CONTRASENA, None)
        limpios = super()._validar(datos)
        if contrasena is not None:
            self.validar_contrasena(contrasena, limpios.get('nombre_usuario', ''))
            limpios['hash_contrasena'] = generar_hash(contrasena)
            # Contraseña nueva: también se quita el bloqueo por intentos fallidos
            limpios['intentos_fallidos'] = 0
            limpios['bloqueado_hasta'] = None
        return limpios

    def _verificar_reglas(self, datos, actual=None):
        if actual is None and 'hash_contrasena' not in datos:
            raise ValueError('La contraseña es obligatoria.')
        # Se revisa otra vez al guardar (la presentación ya lo revisó al pedir el nombre)
        self.verificar_nombre_disponible(datos['nombre_usuario'], actual)

    # ----- Operaciones CRUD protegidas por la sesión -----
    # Polimorfismo: redefinen las de NegocioBase, exigen la sesión y luego
    # llaman a la versión de la clase padre con super().

    def listar(self):
        self.__sesion.exigir()
        return super().listar()

    def buscar(self, texto):
        self.__sesion.exigir()
        return super().buscar(texto)

    def obtener(self, id_texto):
        self.__sesion.exigir()
        return super().obtener(id_texto)

    def crear(self, datos):
        self.__sesion.exigir()
        return super().crear(datos)

    def actualizar(self, registro, datos):
        self.__sesion.exigir()
        exito, mensaje = super().actualizar(registro, datos)
        if exito and self._es_usuario_de_la_sesion(registro):
            self.__sesion.iniciar(registro)  # así la sesión tiene el nombre nuevo
        return exito, mensaje

    def eliminar(self, registro):
        self.__sesion.exigir()
        if self._es_usuario_de_la_sesion(registro):
            return False, 'No puede eliminar el usuario con el que inició sesión.'
        if self.repositorio.contar() <= 1:
            return False, 'No se puede eliminar el último usuario: el sistema quedaría sin acceso.'
        return super().eliminar(registro)

    def _es_usuario_de_la_sesion(self, registro):
        usuario = self.__sesion.usuario
        return usuario is not None and usuario.get_id() == registro.get_id()

    # ----- Primer usuario (crear_usuario.py) -----

    def hay_usuarios(self):
        return self.repositorio.contar() > 0

    def crear_primer_usuario(self, datos):
        """Crea el primer usuario SIN sesión (aún no hay nadie que pueda iniciarla).

        Solo funciona si la tabla está vacía; los demás usuarios se crean desde
        el menú Usuarios, con la sesión iniciada.
        """
        if self.hay_usuarios():
            return False, ('Ya existen usuarios. Inicie sesión y cree los demás desde '
                           'el menú "Usuarios".')
        return super().crear(datos)
