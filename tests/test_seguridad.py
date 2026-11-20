"""Pruebas del inicio de sesión (Evaluación 3): hash, validaciones y bloqueo."""
from datetime import datetime, timedelta

import pytest

from datos.auxiliares.seguridad import generar_hash, verificar_contrasena
from datos.auxiliares.validaciones import (validar_nombre_usuario, validar_contrasena_nueva,
                                           validar_contrasena_ingresada)
from datos.modelos import Usuario
from negocio.negocio_autenticacion import (NegocioAutenticacion, Sesion, ErrorAcceso,
                                           MENSAJE_CREDENCIALES)

CLAVE = 'Colegio2026'


# ----- Hash -----

def test_hash_no_guarda_la_contrasena():
    hash_guardado = generar_hash(CLAVE)
    assert CLAVE not in hash_guardado
    assert hash_guardado.startswith('pbkdf2_sha256$600000$')


def test_misma_contrasena_distinto_hash():
    # La sal aleatoria hace que dos hashes de la misma contraseña sean distintos
    assert generar_hash(CLAVE) != generar_hash(CLAVE)


def test_verificar_contrasena():
    hash_guardado = generar_hash(CLAVE)
    assert verificar_contrasena(CLAVE, hash_guardado)
    assert not verificar_contrasena('colegio2026', hash_guardado)  # distingue mayúsculas


@pytest.mark.parametrize('hash_danado', ['', 'texto', 'md5$1$a$b', 'pbkdf2_sha256$x$y$z', None])
def test_hash_danado_no_lanza_error(hash_danado):
    assert not verificar_contrasena(CLAVE, hash_danado)


# ----- Validaciones de credenciales -----

def test_validar_usuario():
    assert validar_nombre_usuario('  Admin.Colegio ') == 'admin.colegio'


@pytest.mark.parametrize('usuario', ['', '   ', 'ab', "admin' OR '1'='1", 'josé', 'a' * 31])
def test_usuario_invalido(usuario):
    with pytest.raises(ValueError):
        validar_nombre_usuario(usuario)


@pytest.mark.parametrize('clave', ['', '    ', 'x' * 129])
def test_contrasena_ingresada_invalida(clave):
    with pytest.raises(ValueError):
        validar_contrasena_ingresada(clave)


@pytest.mark.parametrize('clave', ['corta1', 'sololetras', '12345678', 'admin1234'])
def test_contrasena_nueva_debil(clave):
    with pytest.raises(ValueError):
        validar_contrasena_nueva(clave, 'admin')


# ----- Inicio de sesión (usa la base de datos de prueba de conftest.py) -----

@pytest.fixture
def autenticacion(base_prueba):
    negocio = NegocioAutenticacion(Sesion())
    exito, mensaje = negocio.crear_usuario('admin', CLAVE)
    assert exito, mensaje
    return negocio


def test_crear_usuario_guarda_solo_hash(autenticacion):
    usuario = Usuario.get(Usuario.nombre_usuario == 'admin')
    assert usuario.hash_contrasena != CLAVE
    assert verificar_contrasena(CLAVE, usuario.hash_contrasena)


def test_no_permite_usuario_repetido(autenticacion):
    exito, mensaje = autenticacion.crear_usuario('ADMIN', 'OtraClave99')
    assert not exito and 'Ya existe' in mensaje


def test_login_correcto_inicia_sesion(autenticacion):
    exito, _ = autenticacion.iniciar_sesion('admin', CLAVE)
    assert exito
    assert autenticacion.sesion.esta_activa()
    assert autenticacion.sesion.usuario.nombre_usuario == 'admin'


def test_mismo_mensaje_si_no_existe_o_clave_mala(autenticacion):
    _, no_existe = autenticacion.iniciar_sesion('noexiste', CLAVE)
    _, clave_mala = autenticacion.iniciar_sesion('admin', 'ClaveMala1')
    assert no_existe == clave_mala == MENSAJE_CREDENCIALES
    assert not autenticacion.sesion.esta_activa()


def test_login_con_campos_vacios(autenticacion):
    exito, mensaje = autenticacion.iniciar_sesion('', '')
    assert not exito and 'vacío' in mensaje


def test_bloqueo_tras_tres_intentos(autenticacion):
    ahora = datetime(2026, 11, 20, 10, 0)
    for _ in range(3):
        autenticacion.iniciar_sesion('admin', 'ClaveMala1', ahora=ahora)
    # Bloqueada: ni con la clave correcta entra
    exito, mensaje = autenticacion.iniciar_sesion('admin', CLAVE, ahora=ahora)
    assert not exito and 'bloqueada' in mensaje
    # Pasados los 5 minutos vuelve a poder entrar
    exito, _ = autenticacion.iniciar_sesion('admin', CLAVE, ahora=ahora + timedelta(minutes=6))
    assert exito


def test_sesion_exigir():
    sesion = Sesion()
    with pytest.raises(ErrorAcceso):
        sesion.exigir()
    sesion.iniciar(object())
    sesion.exigir()  # no lanza error
    sesion.cerrar()
    with pytest.raises(ErrorAcceso):
        sesion.exigir()
