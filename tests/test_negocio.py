"""Pruebas de la capa de negocio con una base de datos de prueba (ver conftest.py)."""
from decimal import Decimal

import pytest

from datos.modelos import Asignatura, Docente, Estudiante, Evaluacion, Calificacion
from negocio.negocio_asignaturas import NegocioAsignaturas
from negocio.negocio_docentes import NegocioDocentes
from negocio.negocio_estudiantes import NegocioEstudiantes
from negocio.negocio_evaluaciones import NegocioEvaluaciones
from negocio.negocio_pagos import NegocioPagos
from negocio.negocio_apoderados import NegocioApoderados
from negocio.negocio_periodos import NegocioPeriodos

ESTUDIANTE_NUEVO = {'rut': '22.333.444-k', 'nombre': 'josé peña',
                    'fecha_nacimiento': '15-03-2009', 'curso': None, 'apoderado': None}


def crear_asignatura():
    return Asignatura.create(nombre='Matemática', codigo='MAT1', horasSemanales=6,
                             docente=Docente.get_by_id(1))


# ----- Estudiantes -----

def test_crear_estudiante(base_prueba):
    exito, mensaje = NegocioEstudiantes().crear(ESTUDIANTE_NUEVO)
    assert exito, mensaje
    nuevo = Estudiante.get(Estudiante.rut == '22333444-K')
    assert nuevo.nombre == 'José Peña'  # el negocio limpia y ordena los datos


def test_no_permite_rut_repetido(base_prueba):
    datos = dict(ESTUDIANTE_NUEVO, rut='21.123.456-3')
    exito, mensaje = NegocioEstudiantes().crear(datos)
    assert not exito
    assert 'Ya existe' in mensaje


def test_validar_campo_avisa_al_tiro(base_prueba):
    with pytest.raises(ValueError):
        NegocioEstudiantes().validar_campo('rut', '21123456-7')


def test_eliminar_estudiante_es_logico(base_prueba):
    negocio = NegocioEstudiantes()
    estudiante = negocio.obtener('1')
    exito, _ = negocio.eliminar(estudiante)
    assert exito
    assert negocio.listar() == []                         # ya no aparece en el listado
    assert Estudiante.get_by_id(1).activo is False        # pero la fila sigue en la tabla
    exito, _ = negocio.crear(dict(ESTUDIANTE_NUEVO, rut='21123456-3'))
    assert not exito                                      # y su RUT sigue reservado


def test_promedio_y_ficha_del_estudiante(base_prueba):
    asignatura = crear_asignatura()
    estudiante = Estudiante.get_by_id(1)
    for nombre, nota in (('Prueba 1', '6.5'), ('Prueba 2', '4.0')):
        evaluacion = Evaluacion.create(nombre=nombre, porcentaje=50, asignatura=asignatura)
        Calificacion.create(nota=Decimal(nota), estudiante=estudiante, evaluacion=evaluacion)
    assert estudiante.obtener_promedio() == Decimal('5.3')  # 5.25 se redondea a 5.3
    ficha = NegocioEstudiantes().ficha(estudiante)
    assert ficha['promedio'] == '5.3'
    assert len(ficha['notas']) == 2


# ----- Eliminación con dependencias -----

def test_no_elimina_docente_con_asignaturas(base_prueba):
    crear_asignatura()
    negocio = NegocioDocentes()
    exito, mensaje = negocio.eliminar(negocio.obtener('1'))
    assert not exito
    assert '1 en asignaturas' in mensaje
    assert Docente.get_or_none(Docente.id_docente == 1) is not None


def test_elimina_docente_sin_dependencias(base_prueba):
    negocio = NegocioDocentes()
    exito, _ = negocio.eliminar(negocio.obtener('1'))
    assert exito
    assert negocio.listar() == []


# ----- Reglas de negocio -----

def test_ponderaciones_no_superan_100(base_prueba):
    asignatura = crear_asignatura()
    negocio = NegocioEvaluaciones()
    datos = {'nombre': 'Prueba 1', 'fecha': '10-09-2026', 'porcentaje': '60',
             'asignatura': asignatura}
    assert negocio.crear(datos)[0]
    exito, mensaje = negocio.crear(dict(datos, nombre='Prueba 2', porcentaje='50'))
    assert not exito
    assert 'Disponible: 40%' in mensaje


def test_relacion_obligatoria(base_prueba):
    datos = {'nombre': 'Prueba 1', 'fecha': '10-09-2026', 'porcentaje': '30',
             'asignatura': None}
    exito, mensaje = NegocioEvaluaciones().crear(datos)
    assert not exito
    assert 'asignatura' in mensaje


def test_un_solo_periodo_activo(base_prueba):
    exito, mensaje = NegocioPeriodos().crear({'anio': '2027', 'semestre': '1',
                                              'estado': 'activo'})
    assert not exito
    assert 'otro periodo Activo' in mensaje


def test_codigo_de_asignatura_se_normaliza(base_prueba):
    exito, _ = NegocioAsignaturas().crear({'nombre': 'Historia', 'codigo': 'his 1',
                                           'horasSemanales': '4', 'docente': None,
                                           'curso': None})
    assert exito
    assert Asignatura.get(Asignatura.nombre == 'Historia').codigo == 'HIS1'


def test_pago_no_se_registra_dos_veces(base_prueba):
    NegocioApoderados().crear({'rut': '12345678-5', 'nombre': 'María González',
                               'telefono': ''})
    negocio_pagos = NegocioPagos()
    apoderado = NegocioApoderados().obtener('1')
    assert negocio_pagos.crear({'apoderado': apoderado, 'monto': '$45.000',
                                'estado': 'Pendiente'})[0]
    pago = negocio_pagos.obtener('1')
    assert negocio_pagos.registrar_pago(pago)[0]
    assert pago.esta_pagado()
    exito, _ = negocio_pagos.registrar_pago(pago)
    assert not exito


# ----- Principios de POO en los modelos -----

def test_polimorfismo_mostrar_datos(base_prueba):
    """Docente y Estudiante heredan de Persona, y cada uno responde mostrar_datos() a su manera."""
    personas = [Docente.get_by_id(1), Estudiante.get_by_id(1)]
    fichas = [persona.mostrar_datos() for persona in personas]
    assert fichas[0].startswith('Docente: Carlos Pérez')
    assert 'Especialidad: Matemáticas' in fichas[0]
    assert fichas[1].startswith('Estudiante: Cristopher Lagos')
    assert 'RUT: 21123456-3' in fichas[1]
