from datos.modelos.base import BaseModel
from datos.modelos.persona import Persona
from datos.modelos.periodo import PeriodoAcademico, ESTADOS_PERIODO
from datos.modelos.curso import Curso, JORNADAS
from datos.modelos.docente import Docente
from datos.modelos.asignatura import Asignatura
from datos.modelos.apoderado import Apoderado
from datos.modelos.estudiante import Estudiante
from datos.modelos.evaluacion import Evaluacion
from datos.modelos.calificacion import Calificacion
from datos.modelos.asistencia import Asistencia
from datos.modelos.pago import Pago, ESTADOS_PAGO

# Modelos que tienen tabla en la base de datos (Persona y BaseModel no tienen).
MODELOS = [PeriodoAcademico, Curso, Docente, Asignatura, Apoderado,
           Estudiante, Evaluacion, Calificacion, Asistencia, Pago]
