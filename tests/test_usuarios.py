"""Pruebas de la gestión de usuarios (Evaluación 3). Usan la base SQLite en memoria."""
import pytest

from datos.auxiliares.seguridad import verificar_contrasena, es_hash_bcrypt
from datos.modelos import Usuario
from negocio.negocio_autenticacion import NegocioAutenticacion, Sesion, ErrorAcceso
from negocio.negocio_usuarios import NegocioUsuarios

CLAVE = 'Colegio2026'


@pytest.fixture
def sesion(base_prueba):
    """Crea el primer usuario 'admin' e inicia sesión con él."""
    exito, mensaje = NegocioUsuarios(Sesion()).crear_primer_usuario(
        {'nombre_usuario': 'admin', 'contrasena': CLAVE})
    assert exito, mensaje
    sesion = Sesion()
    exito, _ = NegocioAutenticacion(sesion).iniciar_sesion('admin', CLAVE)
    assert exito
    return sesion


@pytest.fixture
def usuarios(sesion):
    return NegocioUsuarios(sesion)


def crear(negocio, nombre='secretaria', clave='Secreta2026'):
    return negocio.crear({'nombre_usuario': nombre, 'contrasena': clave})


# ----- Primer usuario (crear_usuario.py) -----

def test_primer_usuario_solo_con_tabla_vacia(sesion):
    exito, mensaje = NegocioUsuarios(Sesion()).crear_primer_usuario(
        {'nombre_usuario': 'otro', 'contrasena': 'OtraClave99'})
    assert not exito and 'Ya existen usuarios' in mensaje


# ----- Registrar -----

def test_registrar_guarda_solo_el_hash(usuarios):
    exito, mensaje = crear(usuarios)
    assert exito, mensaje
    guardado = Usuario.get(Usuario.nombre_usuario == 'secretaria')
    assert es_hash_bcrypt(guardado.hash_contrasena)
    assert 'Secreta2026' not in guardado.hash_contrasena
    assert verificar_contrasena('Secreta2026', guardado.hash_contrasena)


def test_no_permite_nombre_repetido(usuarios):
    exito, mensaje = crear(usuarios, nombre='ADMIN')  # se pasa a minúsculas: 'admin'
    assert not exito and 'Ya existe' in mensaje


def test_contrasena_obligatoria_al_registrar(usuarios):
    exito, mensaje = usuarios.crear({'nombre_usuario': 'secretaria'})
    assert not exito and 'obligatoria' in mensaje


@pytest.mark.parametrize('clave', ['corta1', 'sololetras', 'a1' * 37, 'secretaria2026'])
def test_rechaza_contrasena_invalida(usuarios, clave):
    exito, _ = crear(usuarios, clave=clave)
    assert not exito
    assert not Usuario.select().where(Usuario.nombre_usuario == 'secretaria').exists()


# ----- Listar y buscar: nunca muestran el hash -----

def test_listar_no_muestra_el_hash(usuarios):
    crear(usuarios)
    for usuario in usuarios.listar():
        assert 'hash' not in ' '.join(Usuario.columnas()).lower()
        assert usuario.hash_contrasena not in [str(valor) for valor in usuario.fila()]


def test_buscar(usuarios):
    crear(usuarios)
    assert [u.nombre_usuario for u in usuarios.buscar('secre')] == ['secretaria']


# ----- Actualizar -----

def test_actualizar_nombre_sin_cambiar_contrasena(usuarios):
    crear(usuarios)
    registro = usuarios.buscar('secretaria')[0]
    hash_antes = registro.hash_contrasena
    exito, mensaje = usuarios.actualizar(registro, {'nombre_usuario': 'secretaria2'})
    assert exito, mensaje
    assert Usuario.get_by_id(registro.get_id()).hash_contrasena == hash_antes


def test_cambiar_contrasena_guarda_hash_y_desbloquea(usuarios):
    crear(usuarios)
    registro = usuarios.buscar('secretaria')[0]
    registro.intentos_fallidos = 2
    registro.save()
    exito, _ = usuarios.actualizar(registro, {'nombre_usuario': 'secretaria',
                                              'contrasena': 'Nueva2026x'})
    assert exito
    guardado = Usuario.get_by_id(registro.get_id())
    assert verificar_contrasena('Nueva2026x', guardado.hash_contrasena)
    assert not verificar_contrasena('Secreta2026', guardado.hash_contrasena)
    assert guardado.intentos_fallidos == 0 and guardado.bloqueado_hasta is None


def test_actualizar_a_nombre_existente(usuarios):
    crear(usuarios)
    registro = usuarios.buscar('secretaria')[0]
    exito, mensaje = usuarios.actualizar(registro, {'nombre_usuario': 'admin'})
    assert not exito and 'Ya existe' in mensaje


def test_renombrar_usuario_de_la_sesion_actualiza_la_sesion(usuarios, sesion):
    registro = usuarios.obtener(str(sesion.usuario.get_id()))
    exito, _ = usuarios.actualizar(registro, {'nombre_usuario': 'director'})
    assert exito
    assert sesion.usuario.nombre_usuario == 'director'


# ----- Eliminar -----

def test_no_elimina_usuario_de_la_sesion(usuarios, sesion):
    crear(usuarios)  # hay 2 usuarios, igual no deja borrar el propio
    propio = usuarios.obtener(str(sesion.usuario.get_id()))
    exito, mensaje = usuarios.eliminar(propio)
    assert not exito and 'inició sesión' in mensaje


def test_no_deja_el_sistema_sin_usuarios(base_prueba):
    # Caso límite: sesión de un usuario que ya no está en la tabla y queda uno solo
    NegocioUsuarios(Sesion()).crear_primer_usuario({'nombre_usuario': 'unico',
                                                    'contrasena': CLAVE})
    sesion = Sesion()
    sesion.iniciar(Usuario(id_usuario=999, nombre_usuario='fantasma'))
    negocio = NegocioUsuarios(sesion)
    exito, mensaje = negocio.eliminar(negocio.buscar('unico')[0])
    assert not exito and 'último usuario' in mensaje


def test_eliminar_otro_usuario(usuarios):
    crear(usuarios)
    exito, mensaje = usuarios.eliminar(usuarios.buscar('secretaria')[0])
    assert exito, mensaje
    assert usuarios.buscar('secretaria') == []


# ----- Todo exige sesión -----

@pytest.mark.parametrize('operacion', [
    lambda n: n.listar(),
    lambda n: n.buscar('a'),
    lambda n: n.obtener('1'),
    lambda n: crear(n),
])
def test_sin_sesion_no_hay_acceso(base_prueba, operacion):
    with pytest.raises(ErrorAcceso):
        operacion(NegocioUsuarios(Sesion()))
