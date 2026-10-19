"""Pruebas de las validaciones (datos/auxiliares/validaciones.py). No usan base de datos."""
from datetime import date, timedelta
from decimal import Decimal

import pytest

from datos.auxiliares.validaciones import (
    calcular_dv, normalizar_rut, validar_rut, validar_nombre, validar_fecha_nacimiento,
    validar_codigo, validar_nota, validar_porcentaje, validar_monto, validar_fecha_hasta_hoy)


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


@pytest.mark.parametrize('texto', ['15-05-2010', '15/05/2010', '2010-05-15'])
def test_fecha_nacimiento_valida(texto):
    assert validar_fecha_nacimiento(texto) == date(2010, 5, 15)


@pytest.mark.parametrize('fecha', ['2010-13-01', '31-02-2010', 'ayer', '01-01-1850',
                                   (date.today() + timedelta(days=1)).isoformat()])
def test_fecha_nacimiento_invalida(fecha):
    with pytest.raises(ValueError):
        validar_fecha_nacimiento(fecha)


def test_codigo():
    assert validar_codigo(' mat 1 ') == 'MAT1'
    with pytest.raises(ValueError):
        validar_codigo('mat#1')


@pytest.mark.parametrize('texto, esperado', [('6,5', Decimal('6.5')), ('7', Decimal('7.0')),
                                             ('1.0', Decimal('1.0'))])
def test_nota_valida(texto, esperado):
    assert validar_nota(texto) == esperado


@pytest.mark.parametrize('texto', ['0.9', '7.1', '6.55', 'seis', ''])
def test_nota_invalida(texto):
    with pytest.raises(ValueError):
        validar_nota(texto)


def test_porcentaje():
    assert validar_porcentaje('30') == Decimal('30.00')
    for malo in ('0', '101', '-5'):
        with pytest.raises(ValueError):
            validar_porcentaje(malo)


def test_monto():
    assert validar_monto('$45.000') == 45000
    with pytest.raises(ValueError):
        validar_monto('0')


def test_fecha_hasta_hoy():
    assert validar_fecha_hasta_hoy('') == date.today()
    with pytest.raises(ValueError):
        validar_fecha_hasta_hoy((date.today() + timedelta(days=1)).strftime('%d-%m-%Y'))
