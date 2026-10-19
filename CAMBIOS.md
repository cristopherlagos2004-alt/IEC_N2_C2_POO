# Cambios realizados

# Versión 2.0 (19-10-2026): ajuste a la pauta de la Evaluación 2

**No hay que recrear la base de datos**: las tablas no cambiaron. Basta con actualizar el código.

## 1. Estructura pedida por la pauta
- El diagrama UML pasó a la **raíz** del proyecto (`ev1poo.drawio`). Se agregó la clase abstracta `Persona` con sus flechas de herencia hacia Estudiante, Docente y Apoderado.
- Nueva carpeta **`datos/auxiliares/`**, que reemplaza a `datos/auxiliar.py` y `negocio/validaciones.py`:
  - `validaciones.py`: RUT, nombres, correo, teléfono, notas, porcentajes, montos y fechas
  - `formatos.py`: fechas `DD-MM-AAAA`, montos `$45.000`, notas y porcentajes
  - `calculos.py`: promedio con redondeo chileno (6.45 → 6.5) y porcentaje de asistencia
  - `errores.py`: registro de errores en `errores.log`
- **`datos/conexion.py`** ahora es la clase `Conexion`, con los métodos `conectar()`, `desconectar()` y `esta_conectada()`.

## 2. CRUD de todos los componentes
- El menú principal permite navegar por los **10 componentes**: Estudiantes, Cursos, Docentes, Asignaturas, Apoderados, Periodos, Evaluaciones, Calificaciones, Asistencias y Pagos.
- Cada uno tiene **Listar, Registrar, Buscar, Actualizar y Eliminar**, más opciones propias que usan los métodos del UML:
  - ficha académica del estudiante (promedio, asistencia y notas)
  - estudiantes de un curso
  - asignaturas y estudiantes de un docente
  - promedio de una asignatura
  - ficha del apoderado
  - iniciar o cerrar un periodo
  - registrar un pago
- Los métodos del diagrama UML están implementados en los modelos: `obtenerPromedio()`, `consultarNotas()`, `listarEstudiantes()`, `cerrarPeriodo()`, `registrarPago()`, `validarNota()`, `calcularPromedio()`, etc.

## 3. Principios de POO
- **Abstracción:** clases abstractas `RepositorioBase`, `NegocioBase`, `MenuBase` y `MenuCrud`.
- **Encapsulamiento:** atributos privados (`__repositorio`, `__negocio`, `__base_datos`) con propiedades de solo lectura.
- **Herencia:** `Persona` → Estudiante, Docente y Apoderado. Además, cada repositorio, clase de negocio y menú hereda de su clase base, así que el CRUD se escribe una sola vez.
- **Polimorfismo:** `columnas()`, `fila()` y `mostrar_datos()` distintos en cada modelo. `eliminar()` de estudiantes hace eliminación lógica. El menú principal trata igual a todos los submenús.

## 4. Mejoras de uso
- **Cada dato se valida apenas se escribe**: si está mal, se explica el motivo y se vuelve a pedir, sin tener que llenar todo el formulario.
- Antes de eliminar, se revisa si hay registros que dependen del que se quiere borrar. Por ejemplo: "No se puede eliminar el curso: tiene registros asociados (1 en asignaturas, 2 en estudiantes)".
- Reglas de negocio nuevas:
  - una nota por estudiante en cada evaluación
  - una asistencia por estudiante al día
  - las ponderaciones de una asignatura no pasan de 100%
  - un solo periodo activo
  - un pago no se registra dos veces
- Las fechas se aceptan como `15-05-2010`, `15/05/2010` o `2010-05-15`. Las notas, con coma o punto (`6,5` o `6.5`).

## 5. Pruebas
- **47 pruebas automáticas.** Las de `tests/test_negocio.py` usan una base de datos SQLite en memoria, así que se ejecutan sin MySQL y sin `.env`.

## 6. README
- Encabezado ordenado, estructura de carpetas, tabla de principios de POO y comandos para Windows (`py`).
- Nota sobre `--default-character-set=utf8mb4`, necesaria para que la ñ y los tildes se guarden bien.
- El usuario de MySQL se crea copiando los comandos, **sin editar el script**, para que ninguna contraseña llegue a GitHub.

---

# Versión 1.1 (18-10-2026): corrección de errores

## ⚠️ Lo que el grupo tiene que hacer
1. **Recrear la base de datos**: `DROP DATABASE gestion_escolar;` y ejecutar los scripts de `datos/sql/` en orden de fecha.
2. **Crear el archivo `.env`** copiando `.env.example`. Ahora las variables se llaman `DB_NAME`, `DB_HOST`, `DB_PORT`, `DB_USER` y `DB_PASSWORD`.
3. `pip install -r requirements.txt` (se quitaron librerías que no se usaban).

## 1. Errores que impedían ejecutar el programa
- Los modelos y repositorios importaban `base_datos`, pero `conexion.py` solo tenía `conectar_db` → `ImportError`. Ahora `conexion.py` define `base_datos`.
- Los `ForeignKeyField` no tenían `column_name`. Peewee buscaba columnas como `curso_id` que no existen en las tablas (la tabla usa `id_curso`). Se agregó `column_name` en todas las relaciones.
- El README daba permisos sobre `db_gestion_escolar`, pero la base se llama `gestion_escolar`.

## 2. Código duplicado
- Se eliminó `datos/models.py`. Se dejó un único juego de modelos en `datos/modelos/`, con una clase `BaseModel` común en `base.py` (antes se repetía en los 10 archivos).
- Se unificó la configuración en `datos/auxiliar.py` (antes había dos menús distintos).
- Se eliminó `negocio/gestor_escolar.py`, que no se usaba.

## 3. Arquitectura por capas
- La capa de presentación ya no llama directo al repositorio: ahora solo habla con la capa de negocio.
- Las validaciones están en `negocio/validaciones.py`:
  - RUT con dígito verificador (módulo 11)
  - nombre
  - fecha de nacimiento (formato correcto, no futura)
- Las consultas de Peewee se ejecutan dentro del `try` con `list(...)`. Antes, `select()` devolvía una consulta que recién se ejecutaba fuera del `try`, así que los errores no se capturaban.

## 4. Funcionalidad
- **Eliminar estudiante** ahora funciona y aparece en el menú (opción 5). Usa eliminación lógica: marca `activo = 0` y pide confirmación antes. Antes la función solo volvía a guardar el registro sin cambios.
- Se valida que el RUT no esté repetido, tanto al registrar como al actualizar.
- `main.py` avisa con un mensaje claro si falta el `.env` o si no se puede conectar a MySQL.

## 5. Base de datos (scripts SQL)
- Se eliminó el DDL duplicado `2026.10.18_ddl_gestion_escolar.sql`, que volvía a crear las mismas tablas y fallaba.
- Se corrigió el nombre `2026.16.10_...Alter_Asistencias.sql` a `2026.10.16_...` (el mes 16 no existe).
- Se renombró `periodicos_academicos` a `periodos_academicos` (y `id_periodico` a `id_periodo`).
- **Apoderado–Estudiante**: según el UML, un apoderado tiene muchos estudiantes. La clave foránea se movió a `estudiantes.id_apoderado`. Antes, un apoderado con dos hijos no se podía registrar.
- `pagos.monto`: de `FLOAT` a `INTEGER` (pesos chilenos, sin errores de redondeo).
- `nota` pasó a `DECIMAL(2,1)` y `porcentaje` a `DECIMAL(5,2)`. Se agregaron validaciones `CHECK`:
  - nota entre 1.0 y 7.0
  - porcentaje entre 0 y 100
  - monto mayor que 0
  - semestre 1 o 2
  - estado del periodo válido
- Los periodos ahora se insertan antes que los cursos, y los cursos quedan asociados al periodo 2026-2.
- Se corrigió el estado de los periodos: 2026-1 aparecía "Activo" y 2026-2 "Cerrado", al revés de lo que corresponde.
- Se corrigieron los RUT de prueba, que tenían el dígito verificador incorrecto.

## 6. Seguridad
- La conexión ya no usa por defecto `root` sin contraseña: exige `DB_USER` y `DB_PASSWORD` en el `.env`.
- Hay un nuevo script que crea `usuario_escolar` con **privilegios mínimos** (`SELECT, INSERT, UPDATE, DELETE`). Antes se le daba `ALL PRIVILEGES`.
- Se agregó `.gitignore` para que el `.env` (contraseñas) no se suba a GitHub.
- Los errores de la base de datos ya no se muestran completos en pantalla. Se guardan en `errores.log` y el usuario ve un mensaje genérico.
- `requirements.txt` quedó solo con lo que se usa. Se quitaron 8 librerías que no se usaban (menos superficie de ataque).
- El README explica cómo crear el usuario con privilegios mínimos sobre la base correcta (`gestion_escolar`).

## 7. Diagrama UML (`ev1poo.drawio`)
- "Clasificacion" → "Calificacion"; "periodico academico" → "Periodo Académico".
- Pago: `idpago` → `id`, `monto: float` → `monto: int`. Estudiante: se agregó `activo: bool`.
- La línea Estudiante–Evaluación terminaba en el texto "*" y no en la clase: se reconectó.
- Se eliminaron 4 flechas basura (sin conexión o conectadas a sí mismas) y un texto suelto que no era parte del diagrama.

## 8. Pruebas
- Nuevo `tests/test_validaciones.py` con 20 casos para RUT, nombre y fecha. Se ejecutan con `pytest` desde la carpeta del proyecto (la configuración está en `pytest.ini`).
