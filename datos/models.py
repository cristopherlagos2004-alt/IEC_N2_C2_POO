from peewee import TextField, DateField, AutoField, CharField, IntegerField, FloatField, DateTimeField, SQL, Model
from datos.conexion import conectar_db

database = conectar_db()
defecto = "DEFAULT 1"

class BaseModel(Model):
    class Meta:
        database = database

class PeriodicosAcademicos(BaseModel):
    id_periodico = AutoField()
    anio = IntegerField()
    semestre = IntegerField()
    estado = CharField(max_length=30)

    class Meta:
        table_name = 'periodicos_academicos'

class Docentes(BaseModel):
    id_docente = AutoField()
    nombre = CharField(max_length=100)
    correo = CharField(max_length=100, null=True)
    especialidad = CharField(max_length=100, null=True)

    class Meta:
        table_name = 'docentes'

class Cursos(BaseModel):
    id_curso = AutoField()
    nombre = CharField(max_length=50)
    nivel = IntegerField()
    jornada = CharField(max_length=30)
    id_periodico = IntegerField(index=True, null=True)

    class Meta:
        table_name = 'cursos'

class Asignaturas(BaseModel):
    id_asignatura = AutoField()
    nombre = CharField(max_length=50)
    codigo = CharField(max_length=20)
    horasSemanales = IntegerField()
    id_docente = IntegerField(index=True, null=True)
    id_curso = IntegerField(index=True, null=True)

    class Meta:
        table_name = 'asignaturas'

class Estudiantes(BaseModel):
    id_estudiante = AutoField()
    nombre = CharField(max_length=100)
    rut = CharField(max_length=15, unique=True)
    fecha_nacimiento = DateField(null=True)
    id_curso = IntegerField(index=True, null=True)

    class Meta:
        table_name = 'estudiantes'

class Evaluaciones(BaseModel):
    id_evaluacion = AutoField()
    nombre = CharField(max_length=100)
    fecha = DateField(null=True)
    porcentaje = FloatField()
    id_asignatura = IntegerField(index=True, null=True)

    class Meta:
        table_name = 'evaluaciones'

class Apoderados(BaseModel):
    id_apoderado = AutoField()
    nombre = CharField(max_length=100)
    rut = CharField(max_length=15, unique=True)
    telefono = CharField(max_length=20, null=True)
    id_estudiante = IntegerField(index=True, null=True)

    class Meta:
        table_name = 'apoderados'

class Asistencias(BaseModel):
    id_asistencia = AutoField()
    fecha = DateField()
    presente = IntegerField(constraints=[SQL(defecto)])
    observacion = TextField(null=True)
    id_estudiante = IntegerField(index=True, null=True)

    class Meta:
        table_name = 'asistencias'

class Calificaciones(BaseModel):
    id_calificacion = AutoField()
    nota = FloatField()
    fechaRegistro = DateField(null=True)
    observacion = TextField(null=True)
    id_estudiante = IntegerField(index=True, null=True)
    id_evaluacion = IntegerField(index=True, null=True)

    class Meta:
        table_name = 'calificaciones'

class Pagos(BaseModel):
    id_pago = AutoField()
    monto = FloatField()
    estado = CharField(max_length=30)
    id_apoderado = IntegerField(index=True, null=True)

    class Meta:
        table_name = 'pagos'
