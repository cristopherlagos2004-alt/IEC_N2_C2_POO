"""La capa de presentación nunca importa la capa de datos: todo pasa por negocio."""
import ast
from pathlib import Path

import pytest

PRESENTACION = Path(__file__).resolve().parent.parent / 'presentacion'


@pytest.mark.parametrize('archivo', sorted(PRESENTACION.glob('*.py')), ids=lambda p: p.name)
def test_presentacion_no_importa_datos(archivo):
    arbol = ast.parse(archivo.read_text(encoding='utf-8'))
    for nodo in ast.walk(arbol):
        if isinstance(nodo, ast.ImportFrom):
            modulos = [nodo.module or '']
        elif isinstance(nodo, ast.Import):
            modulos = [alias.name for alias in nodo.names]
        else:
            continue
        for modulo in modulos:
            assert not (modulo == 'datos' or modulo.startswith('datos.')), \
                f'{archivo.name} importa {modulo}'
