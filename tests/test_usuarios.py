"""Pruebas de usuarios, BCrypt y login (usan la base de prueba de conftest.py)."""
import pytest

from auxiliares.seguridad import generar_hash, verificar_clave
from auxiliares.validaciones import validar_clave, validar_nombre_usuario
from datos.modelos import Usuario
from negocio.negocio_usuarios import NegocioUsuarios

NUEVO = {'nombre_usuario': 'Cristopher.Lagos', 'nombre': 'cristopher lagos',
         'clave': 'Segura2026'}


# ----- BCrypt -----

def test_hash_no_es_la_clave_y_se_verifica():
    hash_clave = generar_hash('Segura2026')
    assert hash_clave != 'Segura2026'
    assert hash_clave.startswith('$2b$')
    assert verificar_clave('Segura2026', hash_clave)
    assert not verificar_clave('segura2026', hash_clave)


def test_mismo_clave_da_hash_distinto():
    # La "sal" aleatoria hace que dos hashes de la misma contraseña sean distintos
    assert generar_hash('Segura2026') != generar_hash('Segura2026')


def test_hash_del_script_sql_inicial():
    # Hash que está en datos/sql/2026.11.27_10.15_Insert_Usuario_Inicial.sql
    hash_sql = '$2b$12$RVsUHZteV6nbplYOlKTuq.cpUPBSTPbgKlsHXjuSQ0qFBlkhcKPO6'
    assert verificar_clave('Admin2026!', hash_sql)


# ----- Validaciones -----

@pytest.mark.parametrize('clave', ['corta1', 'sololetras', '12345678', ''])
def test_claves_inseguras(clave):
    with pytest.raises(ValueError):
        validar_clave(clave)


def test_nombre_usuario_se_normaliza():
    assert validar_nombre_usuario('  Admin.Escuela ') == 'admin.escuela'
    with pytest.raises(ValueError):
        validar_nombre_usuario('con espacio')


# ----- CRUD -----

def test_crear_usuario_guarda_hash(base_prueba):
    exito, mensaje = NegocioUsuarios().crear(NUEVO)
    assert exito, mensaje
    usuario = Usuario.get(Usuario.nombre_usuario == 'cristopher.lagos')
    assert usuario.nombre == 'Cristopher Lagos'
    assert usuario.clave_hash != 'Segura2026'            # nunca en texto plano
    assert verificar_clave('Segura2026', usuario.clave_hash)


def test_no_permite_usuario_repetido(base_prueba):
    negocio = NegocioUsuarios()
    assert negocio.crear(NUEVO)[0]
    exito, mensaje = negocio.crear(dict(NUEVO, nombre_usuario='cristopher.lagos'))
    assert not exito
    assert 'Ya existe' in mensaje


def test_actualizar_usuario_no_cambia_la_clave(base_prueba):
    negocio = NegocioUsuarios()
    negocio.crear(NUEVO)
    usuario = negocio.obtener('1')
    hash_antes = usuario.clave_hash
    exito, _ = negocio.actualizar(usuario, {'nombre_usuario': 'clagos', 'nombre': 'Cristopher'})
    assert exito
    assert Usuario.get_by_id(1).nombre_usuario == 'clagos'
    assert Usuario.get_by_id(1).clave_hash == hash_antes


# ----- Login -----

def test_login_correcto_e_incorrecto(base_prueba):
    negocio = NegocioUsuarios()
    negocio.crear(NUEVO)
    assert not negocio.iniciar_sesion('cristopher.lagos', 'otraClave1')[0]
    assert not negocio.iniciar_sesion('no.existe', 'Segura2026')[0]
    assert negocio.usuario_sesion is None
    exito, _ = negocio.iniciar_sesion('CRISTOPHER.LAGOS', 'Segura2026')
    assert exito
    assert negocio.usuario_sesion.nombre_usuario == 'cristopher.lagos'
    assert Usuario.get_by_id(1).ultimo_acceso is not None


def test_mismo_mensaje_si_usuario_no_existe(base_prueba):
    negocio = NegocioUsuarios()
    negocio.crear(NUEVO)
    _, mensaje_clave_mala = negocio.iniciar_sesion('cristopher.lagos', 'otraClave1')
    _, mensaje_no_existe = negocio.iniciar_sesion('no.existe', 'otraClave1')
    assert mensaje_clave_mala == mensaje_no_existe


def test_usuario_deshabilitado_no_puede_entrar(base_prueba):
    negocio = NegocioUsuarios()
    negocio.crear(NUEVO)
    exito, _ = negocio.eliminar(negocio.obtener('1'))
    assert exito
    assert Usuario.get_by_id(1).activo is False           # no se borra la fila
    assert not negocio.iniciar_sesion('cristopher.lagos', 'Segura2026')[0]
    assert negocio.habilitar(negocio.obtener('1'))[0]
    assert negocio.iniciar_sesion('cristopher.lagos', 'Segura2026')[0]


def test_no_se_puede_deshabilitar_a_si_mismo(base_prueba):
    negocio = NegocioUsuarios()
    negocio.crear(NUEVO)
    negocio.iniciar_sesion('cristopher.lagos', 'Segura2026')
    exito, _ = negocio.eliminar(negocio.obtener('1'))
    assert not exito
    assert Usuario.get_by_id(1).activo is True


def test_cambiar_clave_propia_pide_la_actual(base_prueba):
    negocio = NegocioUsuarios()
    negocio.crear(NUEVO)
    negocio.iniciar_sesion('cristopher.lagos', 'Segura2026')
    usuario = negocio.obtener('1')
    assert not negocio.cambiar_clave(usuario, 'Nueva2026x', 'Nueva2026x', 'mala')[0]
    assert not negocio.cambiar_clave(usuario, 'Nueva2026x', 'Distinta1', 'Segura2026')[0]
    assert negocio.cambiar_clave(usuario, 'Nueva2026x', 'Nueva2026x', 'Segura2026')[0]
    assert verificar_clave('Nueva2026x', Usuario.get_by_id(1).clave_hash)


def test_menu_principal_exige_login(base_prueba):
    from presentacion.menu import MenuPrincipal
    with pytest.raises(PermissionError):
        MenuPrincipal(NegocioUsuarios())
