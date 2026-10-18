from datetime import date, timedelta

import pytest

from negocio.validaciones import (calcular_dv, normalizar_rut, validar_rut,
                                  validar_nombre, validar_fecha_nacimiento)


def test_calcular_dv():
    assert calcular_dv('21123456') == '3'
    assert calcular_dv('20987654') == 'K'
    assert calcular_dv('21555444') == '9'


def test_normalizar_rut():
    assert normalizar_rut(' 20.987.654-k ') == '20987654-K'
    assert normalizar_rut('211234563') == '21123456-3'


def test_rut_valido():
    assert validar_rut('21.123.456-3') == '21123456-3'


@pytest.mark.parametrize('rut', ['21123456-7', 'abc', '', '123-4', '21123456-X'])
def test_rut_invalido(rut):
    with pytest.raises(ValueError):
        validar_rut(rut)


def test_nombre_valido():
    assert validar_nombre('  valentina   muñoz ') == 'Valentina Muñoz'


@pytest.mark.parametrize('nombre', ['', '   ', 'Juan123', 'a' * 101, "Robert'); DROP TABLE"])
def test_nombre_invalido(nombre):
    with pytest.raises(ValueError):
        validar_nombre(nombre)


def test_fecha_valida():
    assert validar_fecha_nacimiento('2010-05-15') == date(2010, 5, 15)


@pytest.mark.parametrize('fecha', ['15/05/2010', '2010-13-01', 'ayer', '1850-01-01',
                                   (date.today() + timedelta(days=1)).isoformat()])
def test_fecha_invalida(fecha):
    with pytest.raises(ValueError):
        validar_fecha_nacimiento(fecha)
