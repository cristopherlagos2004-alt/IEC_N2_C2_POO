"""Pruebas de la entrada de contraseñas con maskpass (Evaluación 3).

maskpass lee el teclado de verdad, así que en las pruebas se reemplaza
maskpass.askpass por una función que devuelve respuestas preparadas.
"""
import pytest

from presentacion import consola
from presentacion.consola import OperacionCancelada, pedir_contrasena, pedir_contrasena_nueva


class TerminalFalsa:
    """Simula a alguien escribiendo en una terminal."""

    def __init__(self, monkeypatch, respuestas):
        self.respuestas = list(respuestas)
        self.llamadas = []
        monkeypatch.setattr(consola.sys.stdin, 'isatty', lambda: True, raising=False)
        monkeypatch.setattr(consola.maskpass, 'askpass', self.askpass)

    def askpass(self, prompt='', mask='*'):
        self.llamadas.append((prompt, mask))
        respuesta = self.respuestas.pop(0)
        if isinstance(respuesta, Exception):
            raise respuesta
        return respuesta


def test_usa_maskpass_con_asterisco(monkeypatch):
    terminal = TerminalFalsa(monkeypatch, ['Colegio2026'])
    assert pedir_contrasena('Contraseña') == 'Colegio2026'
    assert terminal.llamadas == [('Contraseña: ', '*')]


def test_letra_cortada_se_vuelve_a_pedir(monkeypatch, capsys):
    error = UnicodeDecodeError('utf-8', b'\xc3', 0, 1, 'unexpected end of data')
    TerminalFalsa(monkeypatch, [error, 'Ñandú2026'])
    assert pedir_contrasena() == 'Ñandú2026'
    assert 'No se pudo leer' in capsys.readouterr().out


def test_sin_terminal_avisa(monkeypatch):
    monkeypatch.setattr(consola.sys.stdin, 'isatty', lambda: False, raising=False)
    with pytest.raises(OperacionCancelada):
        pedir_contrasena()


def _validar(texto):
    if len(texto) < 8:
        raise ValueError('Muy corta.')


def test_contrasena_nueva_repite_si_no_coinciden(monkeypatch, capsys):
    TerminalFalsa(monkeypatch, ['corta', 'Colegio2026', 'Colegio2027', 'Colegio2026', 'Colegio2026'])
    assert pedir_contrasena_nueva(_validar) == 'Colegio2026'
    salida = capsys.readouterr().out
    assert 'Muy corta' in salida and 'no coinciden' in salida
