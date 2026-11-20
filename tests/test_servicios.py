"""Pruebas de los servicios externos (Evaluación 3).

No se conectan a internet: se usa una "sesión HTTP falsa" que devuelve respuestas
preparadas. Así se puede probar qué pasa con un 404, un 500, un timeout, sin
internet, etc., sin depender de que la API esté funcionando.
"""
from datetime import date
from decimal import Decimal
from unittest.mock import Mock

import pytest
import requests

from datos.servicios.cache_local import CacheLocal
from datos.servicios.cliente_http import ClienteHttp
from datos.servicios.errores_servicio import (
    ErrorConfiguracion, ErrorConexionServicio, ErrorTiempoEspera, ErrorCredencialesApi,
    ErrorNoEncontrado, ErrorLimiteConsultas, ErrorServidorApi, ErrorRespuestaInvalida,
    ErrorSolicitud, ocultar_secretos)
from datos.servicios.servicio_clima import ServicioClima
from datos.servicios.servicio_indicadores import ServicioIndicadores
from negocio.negocio_autenticacion import Sesion, ErrorAcceso
from negocio.negocio_servicios import NegocioServiciosExternos, evaluar_actividad
from datos.auxiliares.errores import ErrorDatos

LLAVE = '0123456789abcdef0123456789abcdef'
HOY = date(2026, 11, 20)

RESPUESTA_DOLAR = {'codigo': 'dolar', 'nombre': 'Dólar observado', 'serie': [
    {'fecha': '2026-11-21T03:00:00.000Z', 'valor': 999.0},   # día futuro: se descarta
    {'fecha': '2026-11-20T03:00:00.000Z', 'valor': 950.5},
    {'fecha': '2026-11-19T03:00:00.000Z', 'valor': 948.1},
]}
RESPUESTA_CLIMA = {
    'weather': [{'id': 800, 'main': 'Clear', 'description': 'cielo claro'}],
    'main': {'temp': 18.2, 'feels_like': 17.5, 'humidity': 60},
    'wind': {'speed': 3.1}, 'sys': {'country': 'CL'}, 'name': 'Temuco',
}


def respuesta(codigo=200, json_datos=None, tipo='application/json'):
    falsa = Mock()
    falsa.status_code = codigo
    falsa.headers = {'Content-Type': tipo}
    falsa.json.return_value = json_datos
    return falsa


def cliente_con(*resultados):
    """ClienteHttp cuya sesión devuelve (o lanza) los resultados en orden."""
    sesion = Mock()
    sesion.get.side_effect = list(resultados)
    cliente = ClienteHttp('prueba', 'https://api.prueba.cl', sesion_http=sesion,
                          esperar=lambda segundos: None)  # no espera de verdad
    return cliente, sesion


# ----- ClienteHttp: códigos HTTP y errores de red -----

def test_respuesta_correcta_y_timeout_configurado():
    cliente, sesion = cliente_con(respuesta(200, {'ok': 1}))
    assert cliente.obtener_json('dato', {'a': 1}) == {'ok': 1}
    _, kwargs = sesion.get.call_args
    assert kwargs['timeout'] is not None  # nunca sin timeout


@pytest.mark.parametrize('codigo, error', [
    (400, ErrorSolicitud), (401, ErrorCredencialesApi), (403, ErrorCredencialesApi),
    (404, ErrorNoEncontrado), (418, Exception)])
def test_codigos_de_error_sin_reintento(codigo, error):
    cliente, sesion = cliente_con(respuesta(codigo))
    with pytest.raises(error):
        cliente.obtener_json('dato')
    assert sesion.get.call_count == 1  # estos errores no se arreglan reintentando


@pytest.mark.parametrize('codigo, error', [(429, ErrorLimiteConsultas), (500, ErrorServidorApi),
                                           (503, ErrorServidorApi)])
def test_reintenta_y_luego_falla(codigo, error):
    cliente, sesion = cliente_con(respuesta(codigo), respuesta(codigo))
    with pytest.raises(error):
        cliente.obtener_json('dato')
    assert sesion.get.call_count == 2


def test_reintento_que_funciona():
    cliente, _ = cliente_con(respuesta(503), respuesta(200, {'ok': 1}))
    assert cliente.obtener_json('dato') == {'ok': 1}


def test_timeout():
    cliente, _ = cliente_con(requests.exceptions.ReadTimeout(), requests.exceptions.ReadTimeout())
    with pytest.raises(ErrorTiempoEspera):
        cliente.obtener_json('dato')


def test_sin_conexion_no_expone_la_llave():
    url = f'https://api.prueba.cl/weather?q=Temuco&appid={LLAVE}'
    error_red = requests.exceptions.ConnectionError(f'Max retries exceeded with url: {url}')
    cliente, _ = cliente_con(error_red, error_red)
    with pytest.raises(ErrorConexionServicio) as capturado:
        cliente.obtener_json('weather')
    assert LLAVE not in str(capturado.value)
    assert capturado.value.__cause__ is None  # no queda pegado el error original


@pytest.mark.parametrize('falsa', [
    respuesta(200, None, tipo='text/html'),       # no es JSON
    respuesta(200, ['lista'], tipo='application/json'),  # JSON que no es objeto
])
def test_respuesta_no_util(falsa):
    cliente, _ = cliente_con(falsa)
    with pytest.raises(ErrorRespuestaInvalida):
        cliente.obtener_json('dato')


def test_json_mal_formado():
    falsa = respuesta(200)
    falsa.json.side_effect = ValueError('Expecting value')
    cliente, _ = cliente_con(falsa)
    with pytest.raises(ErrorRespuestaInvalida):
        cliente.obtener_json('dato')


def test_solo_https():
    with pytest.raises(ErrorConfiguracion):
        ClienteHttp('prueba', 'http://api.prueba.cl')


def test_ocultar_secretos():
    texto = f'url: https://x.cl/weather?q=Temuco&appid={LLAVE}&units=metric'
    assert ocultar_secretos(texto) == 'url: https://x.cl/weather?q=Temuco&appid=***&units=metric'


# ----- Indicadores (mindicador.cl) -----

def servicio_indicadores(tmp_path, *resultados):
    cliente, sesion = cliente_con(*resultados)
    cache = CacheLocal(tmp_path / 'cache.json')
    return ServicioIndicadores(cliente, cache, hoy=lambda: HOY), sesion


def test_extrae_valor_de_hoy(tmp_path):
    servicio, _ = servicio_indicadores(tmp_path, respuesta(200, RESPUESTA_DOLAR))
    indicador = servicio.obtener('USD')
    assert indicador.codigo == 'dolar'
    assert indicador.valor == Decimal('950.5')  # no el del día futuro
    assert indicador.fecha == HOY
    assert not indicador.desde_cache


def test_moneda_fuera_de_lista_blanca_no_llama_a_la_api(tmp_path):
    servicio, sesion = servicio_indicadores(tmp_path)
    with pytest.raises(ValueError):
        servicio.obtener('../../admin')
    sesion.get.assert_not_called()


@pytest.mark.parametrize('datos', [
    {}, {'serie': []}, {'serie': [{'fecha': '2026-11-20', 'valor': 'abc'}]},
    {'serie': [{'fecha': '2026-11-20', 'valor': -5}]}, {'serie': [{'valor': 900}]},
])
def test_respuesta_con_datos_malos(tmp_path, datos):
    servicio, _ = servicio_indicadores(tmp_path, respuesta(200, datos))
    with pytest.raises(ErrorRespuestaInvalida):
        servicio.obtener('dolar')


def test_usa_cache_si_la_api_falla(tmp_path):
    error_red = requests.exceptions.ConnectionError('sin red')
    servicio, _ = servicio_indicadores(tmp_path, respuesta(200, RESPUESTA_DOLAR),
                                       error_red, error_red)
    servicio.obtener('dolar')                 # 1ª consulta: guarda en caché
    indicador = servicio.obtener('dolar')     # 2ª consulta: sin red -> caché
    assert indicador.desde_cache
    assert indicador.valor == Decimal('950.5')


def test_sin_cache_y_sin_red_lanza_error(tmp_path):
    error_red = requests.exceptions.ConnectionError('sin red')
    servicio, _ = servicio_indicadores(tmp_path, error_red, error_red)
    with pytest.raises(ErrorConexionServicio):
        servicio.obtener('dolar')


def test_cache_danada_se_ignora(tmp_path):
    (tmp_path / 'cache.json').write_text('{esto no es json', encoding='utf-8')
    assert CacheLocal(tmp_path / 'cache.json').leer('dolar') is None


# ----- Clima (OpenWeatherMap) -----

def test_clima_extrae_datos_y_envia_parametros():
    cliente, sesion = cliente_con(respuesta(200, RESPUESTA_CLIMA))
    clima = ServicioClima(cliente, llave=LLAVE).obtener('  temuco ', '')
    assert (clima.ciudad, clima.pais, clima.temperatura, clima.humedad) == ('Temuco', 'CL', 18.2, 60)
    _, kwargs = sesion.get.call_args
    assert kwargs['params']['q'] == 'Temuco,CL'
    assert kwargs['params']['units'] == 'metric'


@pytest.mark.parametrize('ciudad', ['', 'T', 'Temuco,AR', 'Temuco&appid=otra', '<script>', '1234'])
def test_ciudad_invalida_no_llama_a_la_api(ciudad):
    cliente, sesion = cliente_con()
    with pytest.raises(ValueError):
        ServicioClima(cliente, llave=LLAVE).obtener(ciudad)
    sesion.get.assert_not_called()


def test_ciudad_no_encontrada():
    cliente, _ = cliente_con(respuesta(404))
    with pytest.raises(ErrorNoEncontrado) as capturado:
        ServicioClima(cliente, llave=LLAVE).obtener('Ciudad Inventada')
    assert 'No se encontró la ciudad' in str(capturado.value)


def test_clima_con_valores_imposibles():
    datos = dict(RESPUESTA_CLIMA, main={'temp': 500, 'feels_like': 0, 'humidity': 60})
    cliente, _ = cliente_con(respuesta(200, datos))
    with pytest.raises(ErrorRespuestaInvalida):
        ServicioClima(cliente, llave=LLAVE).obtener('Temuco')


def test_falta_llave_en_env(monkeypatch):
    monkeypatch.setenv('OPENWEATHER_API_KEY', 'cambiar_esta_llave')
    cliente, sesion = cliente_con()
    with pytest.raises(ErrorConfiguracion):
        ServicioClima(cliente).obtener('Temuco')
    sesion.get.assert_not_called()


# ----- Negocio: control de sesión y reglas -----

def negocio_con_sesion(activa=True, indicadores=None, clima=None):
    sesion = Sesion()
    if activa:
        sesion.iniciar(object())
    return NegocioServiciosExternos(sesion, indicadores or Mock(), clima or Mock())


@pytest.mark.parametrize('metodo, argumentos', [
    ('indicadores_del_dia', ()), ('pesos_a_moneda', ('45000', 'uf')),
    ('moneda_a_pesos', ('2', 'uf')), ('clima_para_actividad', ('Temuco',))])
def test_sin_sesion_no_se_consume_ninguna_api(metodo, argumentos):
    indicadores, clima = Mock(), Mock()
    negocio = negocio_con_sesion(False, indicadores, clima)
    with pytest.raises(ErrorAcceso):
        getattr(negocio, metodo)(*argumentos)
    indicadores.obtener.assert_not_called()
    clima.obtener.assert_not_called()


def test_conversiones(tmp_path):
    servicio, _ = servicio_indicadores(tmp_path, respuesta(200, RESPUESTA_DOLAR),
                                       respuesta(200, RESPUESTA_DOLAR))
    negocio = negocio_con_sesion(indicadores=servicio)
    _, pesos, dolares = negocio.pesos_a_moneda('$95.050', 'dólar')
    assert (pesos, dolares) == (95050, Decimal('100.00'))
    _, cantidad, pesos = negocio.moneda_a_pesos('2,5', 'usd')
    assert (cantidad, pesos) == (Decimal('2.50'), 2376)  # 2,5 x 950,5 = 2376,25


def test_dato_invalido_se_muestra_como_error_de_usuario():
    negocio = negocio_con_sesion()
    with pytest.raises(ErrorDatos):
        negocio.pesos_a_moneda('-100', 'uf')


def test_un_indicador_que_falla_no_detiene_los_demas():
    indicadores = Mock()
    indicadores.obtener.side_effect = [Mock(), ErrorServidorApi(), Mock(), Mock()]
    lista, errores = negocio_con_sesion(indicadores=indicadores).indicadores_del_dia()
    assert len(lista) == 3 and len(errores) == 1


@pytest.mark.parametrize('codigo, temperatura, viento, apta', [
    (800, 18, 3, True), (500, 18, 3, False), (211, 18, 3, False), (800, 35, 3, False),
    (800, 1, 3, False), (800, 18, 15, False), (741, 18, 3, True)])
def test_evaluar_actividad(codigo, temperatura, viento, apta):
    clima = Mock(codigo_condicion=codigo, temperatura=temperatura, viento=viento)
    assert evaluar_actividad(clima)[0] is apta
