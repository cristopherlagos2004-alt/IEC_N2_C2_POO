# Sistema de Gestión Escolar - POO INACAP

**Desarrollo de Proyecto de Programación Orientada a Objetos**

- **Alumnos:** Cristopher Alexis Lagos Ancan, Alexander Bombin Figueroa
- **Carrera:** Ingeniería / Ciberseguridad - INACAP (Segundo Semestre 2026)

---

## Descripción del Proyecto
Sistema de consola para gestionar un colegio. Está diseñado con una **arquitectura por capas** (Datos, Negocio y Presentación), aplicando Programación Orientada a Objetos en Python y conectándose a una base de datos MySQL mediante el ORM Peewee.

Está basado en nuestro diagrama de clases UML (`ev1poo.drawio`, en la raíz del proyecto), que incluye las entidades Persona, Estudiante, Docente, Apoderado, Curso, Asignatura, Evaluación, Calificación, Asistencia, Pago y Periodo Académico.

Desde el menú principal se puede navegar por los 10 componentes del sistema y hacer en cada uno las operaciones **CRUD**: listar, registrar, buscar, actualizar y eliminar.

## Estructura Modular
```
IEC_N2_C2_POO/
├── main.py              ← inicia la aplicación
├── ev1poo.drawio        ← diagrama de clases UML
├── datos/               ← capa de datos
│   ├── conexion.py      ← clase Conexion (conexión a MySQL)
│   ├── modelos/         ← una clase por entidad del UML
│   ├── repositorio/     ← persistencia y acceso a la información (CRUD con Peewee)
│   ├── sql/             ← scripts para crear y mantener la base de datos
│   └── auxiliares/      ← validaciones, formatos, cálculos y manejo de errores
├── negocio/             ← reglas de negocio de cada entidad
├── presentacion/        ← menús de consola
└── tests/               ← pruebas automáticas
```
- **`datos/`** aísla el manejo de datos: si cambia la base de datos, el resto del sistema no se ve afectado.
- **`negocio/`** valida los datos y aplica las reglas (por ejemplo: RUT no repetido, notas entre 1.0 y 7.0, ponderaciones que no pasen de 100%, un solo periodo activo).
- **`presentacion/`** solo pide datos y muestra resultados; toda la lógica la delega a la capa de negocio.

## Principios de POO aplicados
| Principio | Dónde se aplica |
|---|---|
| **Abstracción** | `RepositorioBase`, `NegocioBase`, `MenuBase` y `MenuCrud` son clases abstractas (`ABC`): definen *qué* se puede hacer y ocultan el *cómo*. La clase `Conexion` oculta los detalles de MySQL. |
| **Encapsulamiento** | Atributos privados (`__repositorio`, `__negocio`, `__base_datos`, `__titulo`) a los que solo se accede con propiedades de lectura (`@property`). |
| **Herencia** | `Persona` → `Estudiante`, `Docente` y `Apoderado`. `BaseModel` → todos los modelos. Cada repositorio, clase de negocio y menú hereda de su clase base, y así no se repite el CRUD 10 veces. |
| **Polimorfismo** | Cada modelo implementa a su manera `columnas()`, `fila()` y `mostrar_datos()`, y una misma función muestra cualquier modelo en una tabla. `RepositorioEstudiantes` redefine `eliminar()` para hacer una eliminación lógica. El menú principal trata igual a los 10 submenús. |

---

## Control de Base de Datos y Configuración
Para conectarnos a la base de datos desde nuestra aplicación usamos el ORM *Peewee* y el driver *PyMySQL*.

### 1. Crear la base de datos
Entramos a MySQL como `root`:
```bash
mysql -u root -p --default-character-set=utf8mb4
```
> En Windows, la opción `--default-character-set=utf8mb4` es necesaria. Sin ella, la ñ y los tildes de los datos de prueba se guardan mal.

Luego ejecutamos los scripts de `datos/sql/` **en orden de fecha** (el nombre de cada archivo indica su orden):
```sql
SOURCE datos/sql/2026.09.11_09.40_ddl_gestion_escolar.sql;
SOURCE datos/sql/2026.09.11_10.30_Insert_Periodos.sql;
SOURCE datos/sql/2026.09.11_10.45_Insert_Cursos.sql;
SOURCE datos/sql/2026.09.14_11.05_Insert_Docentes.sql;
SOURCE datos/sql/2026.09.21_10.30_Insert_Estudiantes.sql;
SOURCE datos/sql/2026.10.09_09.45_Alter_Estudiantes.sql;
SOURCE datos/sql/2026.10.16_10.10_Alter_Asistencias.sql;
```

### 2. Crear el usuario de la aplicación
El script `2026.10.18_20.00_Usuario_Aplicacion.sql` muestra cómo crear el usuario. **No editamos ese archivo**, para que la contraseña no termine en GitHub. En su lugar, copiamos estos comandos en MySQL poniendo nuestra propia contraseña:
```sql
CREATE USER IF NOT EXISTS 'usuario_escolar'@'localhost'
    IDENTIFIED WITH caching_sha2_password BY 'cambiar_esta_contraseña';
GRANT SELECT, INSERT, UPDATE, DELETE ON gestion_escolar.* TO 'usuario_escolar'@'localhost';
FLUSH PRIVILEGES;
```
Le damos solo **los privilegios mínimos** que la aplicación necesita (leer, insertar, modificar y eliminar datos). No usamos `ALL PRIVILEGES`, porque eso permitiría borrar tablas o cambiar la estructura de la base.

### 3. Configurar la conexión (`.env`)
Copiamos el archivo `.env.example` con el nombre `.env` y completamos los datos de conexión:
```
DB_NAME=gestion_escolar
DB_HOST=localhost
DB_PORT=3306
DB_USER=usuario_escolar
DB_PASSWORD=tu_contraseña
```

---

## Control de dependencias (`requirements.txt`)
Para instalar todas las librerías necesarias (Peewee, PyMySQL, PrettyTable, python-decouple, pytest y cryptography), ejecutamos en la terminal:
```bash
pip install -r requirements.txt
```

## Ejecución y pruebas
Para iniciar el sistema:
```bash
python main.py
```
Para ejecutar las pruebas automáticas (usan una base de datos de prueba en memoria, así que no necesitan MySQL ni `.env`):
```bash
pytest
```
> **En Windows**, si `python` o `pip` no se reconocen, usamos `py main.py`, `py -m pip install -r requirements.txt` y `py -m pytest`.
