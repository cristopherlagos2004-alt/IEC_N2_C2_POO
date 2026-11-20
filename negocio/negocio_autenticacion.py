"""Inicio de sesión y control de la sesión activa (Evaluación 3)."""
from datetime import datetime, timedelta

from datos.auxiliares.errores import ErrorDatos
from datos.auxiliares.seguridad import generar_hash, verificar_contrasena, hash_falso
from datos.auxiliares.validaciones import (validar_nombre_usuario, validar_contrasena_ingresada,
                                           validar_contrasena_nueva)
from datos.repositorio.repositorio_usuarios import RepositorioUsuarios

MAX_INTENTOS = 3
MINUTOS_BLOQUEO = 5
# Mismo mensaje para "usuario no existe" y "contraseña incorrecta":
# así nadie puede averiguar qué usuarios existen probando nombres.
MENSAJE_CREDENCIALES = 'Usuario o contraseña incorrectos.'


class ErrorAcceso(ErrorDatos):
    """Se intenta usar una función protegida sin haber iniciado sesión."""


class Sesion:
    """Guarda quién inició sesión.

    Encapsulamiento: el usuario es un atributo privado (__usuario). Solo se
    cambia con iniciar() y cerrar(); desde afuera solo se puede leer.
    """

    def __init__(self):
        self.__usuario = None

    @property
    def usuario(self):
        return self.__usuario

    def iniciar(self, usuario):
        self.__usuario = usuario

    def cerrar(self):
        self.__usuario = None

    def esta_activa(self):
        return self.__usuario is not None

    def exigir(self):
        """Lanza ErrorAcceso si no hay sesión. Lo llaman las funciones protegidas."""
        if not self.esta_activa():
            raise ErrorAcceso('Debe iniciar sesión para usar esta función.')


class NegocioAutenticacion:
    def __init__(self, sesion, repositorio=None):
        self.__sesion = sesion
        self.__repositorio = repositorio or RepositorioUsuarios()

    @property
    def sesion(self):
        return self.__sesion

    def iniciar_sesion(self, nombre_texto, contrasena_texto, ahora=None):
        """Revisa las credenciales. Devuelve (exito, mensaje).

        Reglas:
        - campos vacíos o con formato inválido se rechazan antes de ir a la base de datos
        - el mensaje de error es el mismo si el usuario no existe o si la contraseña está mal
        - después de MAX_INTENTOS fallidos, la cuenta se bloquea MINUTOS_BLOQUEO minutos
        """
        ahora = ahora or datetime.now()
        try:
            nombre = validar_nombre_usuario(nombre_texto)
            contrasena = validar_contrasena_ingresada(contrasena_texto)
        except ValueError as error:
            return False, str(error)

        usuario = self.__repositorio.obtener_por_nombre(nombre)
        if usuario is None:
            verificar_contrasena(contrasena, hash_falso())  # gasta el mismo tiempo
            return False, MENSAJE_CREDENCIALES

        if usuario.esta_bloqueado(ahora):
            return False, ('La cuenta está bloqueada temporalmente por intentos fallidos. '
                           f'Intente en {MINUTOS_BLOQUEO} minutos.')

        if not verificar_contrasena(contrasena, usuario.hash_contrasena):
            usuario.intentos_fallidos += 1
            if usuario.intentos_fallidos >= MAX_INTENTOS:
                usuario.bloqueado_hasta = ahora + timedelta(minutes=MINUTOS_BLOQUEO)
                usuario.intentos_fallidos = 0
            self.__repositorio.guardar(usuario)
            return False, MENSAJE_CREDENCIALES

        usuario.intentos_fallidos = 0
        usuario.bloqueado_hasta = None
        self.__repositorio.guardar(usuario)
        self.__sesion.iniciar(usuario)
        return True, f'Bienvenido(a), {usuario.nombre_usuario}.'

    def cerrar_sesion(self):
        self.__sesion.cerrar()

    def crear_usuario(self, nombre_texto, contrasena_texto):
        """Crea un usuario guardando solo el hash. Devuelve (exito, mensaje)."""
        try:
            nombre = validar_nombre_usuario(nombre_texto)
            contrasena = validar_contrasena_nueva(contrasena_texto, nombre)
        except ValueError as error:
            return False, str(error)
        if self.__repositorio.existe_nombre(nombre):
            return False, f'Ya existe el usuario "{nombre}".'
        usuario = self.__repositorio.modelo(nombre_usuario=nombre,
                                            hash_contrasena=generar_hash(contrasena))
        self.__repositorio.guardar(usuario)
        return True, f'Se creó el usuario "{nombre}".'
