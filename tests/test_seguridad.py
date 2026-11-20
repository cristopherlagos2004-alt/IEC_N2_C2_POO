"""Pruebas del inicio de sesión (Evaluación 3): hash, validaciones y bloqueo."""
from datetime import datetime, timedelta

import pytest

from datos.auxiliares import seguridad
from datos.auxiliares.seguridad import generar_hash, verificar_contrasena, es_hash_bcrypt
from datos.auxiliares.validaciones import (validar_nombre_usuario, validar_contrasena_nueva,
                                           validar_contrasena_ingresada)
from datos.modelos import Usuario
from negocio.negocio_autenticacion import (NegocioAutenticacion, Sesion, ErrorAcceso,
                                           MENSAJE_CREDENCIALES)
from negocio.negocio_usuarios import NegocioUsuarios

CLAVE = 'Colegio2026'
# Hash PBKDF2 como los que guardaba la versión anterior (antes de bcrypt)
HASH_PBKDF2 = ('pbkdf2_sha256$600000$c2FsLWRlLXBydWViYQ==$'
               'aGFzaC1kZS1wcnVlYmEtY29uLTMyLWJ5dGVzLi4uLi4=')


# ----- Hash bcrypt -----

def test_hash_no_guarda_la_contrasena():
    hash_guardado = generar_hash(CLAVE)
    assert CLAVE not in hash_guardado
    assert hash_guardado.startswith('$2b$')   # formato bcrypt
    assert len(hash_guardado) == 60
    assert es_hash_bcrypt(hash_guardado)


def test_costo_por_defecto():
    # Las pruebas usan costo 4 para ir rápido (conftest.py); el programa usa 12
    assert seguridad.COSTO_PRODUCCION == 12


def test_misma_contrasena_distinto_hash():
    # La sal aleatoria hace que dos hashes de la misma contraseña sean distintos
    assert generar_hash(CLAVE) != generar_hash(CLAVE)


def test_verificar_contrasena():
    hash_guardado = generar_hash(CLAVE)
    assert verificar_contrasena(CLAVE, hash_guardado)
    assert not verificar_contrasena('colegio2026', hash_guardado)  # distingue mayúsculas


def test_verificar_con_tildes_y_enie():
    clave = 'Ñandú2026 café'
    assert verificar_contrasena(clave, generar_hash(clave))


@pytest.mark.parametrize('hash_danado', ['', 'texto', 'md5$1$a$b', '$2b$12$corto', None, HASH_PBKDF2])
def test_hash_danado_o_antiguo_no_lanza_error(hash_danado):
    # Un hash PBKDF2 de la versión anterior ya no sirve: se rechaza sin error
    assert not verificar_contrasena(CLAVE, hash_danado)
    assert not es_hash_bcrypt(hash_danado)


def test_limite_72_bytes_en_el_hash():
    assert verificar_contrasena('a' * 72, generar_hash('a' * 72))
    with pytest.raises(ValueError):
        generar_hash('a' * 73)
    # Al verificar no lanza error: simplemente no coincide
    assert not verificar_contrasena('a' * 73, generar_hash('a' * 72))


def test_no_ignora_lo_que_pasa_de_72_bytes():
    # Sin la validación, bcrypt trataría igual "72 aes + X" y "72 aes + Y"
    with pytest.raises(ValueError):
        validar_contrasena_ingresada('a' * 72 + 'X')


# ----- Validaciones de credenciales -----

def test_validar_usuario():
    assert validar_nombre_usuario('  Admin.Colegio ') == 'admin.colegio'


@pytest.mark.parametrize('usuario', ['', '   ', 'ab', "admin' OR '1'='1", 'josé', 'a' * 31])
def test_usuario_invalido(usuario):
    with pytest.raises(ValueError):
        validar_nombre_usuario(usuario)


@pytest.mark.parametrize('clave', ['', '    ', 'x' * 73, 'ñ' * 37, 'ab\x00cd', 'clave\tcon tab'])
def test_contrasena_ingresada_invalida(clave):
    # 'ñ' * 37 son 37 letras pero 74 bytes; el byte nulo y el Tab son caracteres de control
    with pytest.raises(ValueError):
        validar_contrasena_ingresada(clave)


@pytest.mark.parametrize('clave', ['x' * 72, 'ñ' * 36, 'con espacios 1'])
def test_contrasena_ingresada_valida(clave):
    assert validar_contrasena_ingresada(clave) == clave


@pytest.mark.parametrize('clave', ['corta1', 'sololetras', '12345678', 'admin1234'])
def test_contrasena_nueva_debil(clave):
    with pytest.raises(ValueError):
        validar_contrasena_nueva(clave, 'admin')


# ----- Inicio de sesión (usa la base de datos de prueba de conftest.py) -----

@pytest.fixture
def autenticacion(base_prueba):
    exito, mensaje = NegocioUsuarios(Sesion()).crear_primer_usuario(
        {'nombre_usuario': 'admin', 'contrasena': CLAVE})
    assert exito, mensaje
    return NegocioAutenticacion(Sesion())


def test_crear_usuario_guarda_solo_hash(autenticacion):
    usuario = Usuario.get(Usuario.nombre_usuario == 'admin')
    assert usuario.hash_contrasena != CLAVE
    assert es_hash_bcrypt(usuario.hash_contrasena)
    assert verificar_contrasena(CLAVE, usuario.hash_contrasena)


def test_usuario_con_hash_pbkdf2_antiguo_no_entra(autenticacion):
    # Los usuarios creados antes de bcrypt deben volver a crearse (ver README)
    Usuario.update(hash_contrasena=HASH_PBKDF2).execute()
    exito, mensaje = autenticacion.iniciar_sesion('admin', CLAVE)
    assert not exito and mensaje == MENSAJE_CREDENCIALES


def test_mensaje_igual_con_contrasena_larga(autenticacion):
    # Pasarse de 72 bytes da un aviso de formato, sin revelar si el usuario existe
    _, existe = autenticacion.iniciar_sesion('admin', 'a' * 80)
    _, no_existe = autenticacion.iniciar_sesion('noexiste', 'a' * 80)
    assert existe == no_existe


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
