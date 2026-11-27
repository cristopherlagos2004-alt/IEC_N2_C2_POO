# Sistema de Gestión Escolar - POO INACAP

**Desarrollo de Proyecto de Programación Orientada a Objetos**

- **Alumnos:** Cristopher Alexis Lagos Ancan, Alexander Bombin Figueroa
- **Carrera:** Ingeniería / Ciberseguridad - INACAP (Segundo Semestre 2026)

---

## Descripción del Proyecto
Sistema de consola para gestionar un colegio. Está diseñado con una **arquitectura por capas** (Datos, Negocio y Presentación), aplicando Programación Orientada a Objetos en Python y conectándose a una base de datos MySQL mediante el ORM Peewee.

Está basado en nuestro diagrama de clases UML (`ev1poo.drawio`, en la raíz del proyecto), que incluye las entidades Persona, Estudiante, Docente, Apoderado, Curso, Asignatura, Evaluación, Calificación, Asistencia, Pago y Periodo Académico.

La aplicación **parte con un inicio de sesión (login)**: sin usuario y contraseña válidos no se puede llegar al menú principal. Las contraseñas se escriben ocultas (**Maskpass**) y se guardan como hash (**BCrypt**), nunca en texto plano.

Desde el menú principal se puede navegar por los 11 componentes del sistema (los 10 del UML + **Usuarios**) y hacer en cada uno las operaciones **CRUD**: listar, registrar, buscar, actualizar y eliminar (o deshabilitar).

```
Aplicación → Login → Validación (BCrypt) → Menú Principal
```

## Estructura Modular
```
IEC_N2_C2_POO/
├── main.py              ← inicia la aplicación (login → menú principal)
├── ev1poo.drawio        ← diagrama de clases UML
├── datos/               ← capa de datos
│   ├── conexion.py      ← clase Conexion (conexión a MySQL)
│   ├── model_base.py    ← clase ModelBase: configuración común de todos los modelos
│   ├── modelos/         ← una clase por entidad (todas heredan de ModelBase)
│   ├── repositorio/     ← un repositorio por entidad, hecho con FUNCIONES (guardar con save(), listar, buscar...)
│   └── sql/             ← scripts para crear y mantener la base de datos
├── negocio/             ← reglas de negocio y validaciones de cada entidad (incluye el login)
├── presentacion/        ← login, menús y captura de datos por consola
├── auxiliares/          ← validaciones, constantes, mensajes, formatos, seguridad (BCrypt) y errores
└── tests/               ← pruebas automáticas
```
- **`datos/`** aísla el manejo de datos: si cambia la base de datos, el resto del sistema no se ve afectado.
- **`negocio/`** valida los datos y aplica las reglas (por ejemplo: RUT no repetido, notas entre 1.0 y 7.0, ponderaciones que no pasen de 100%, un solo periodo activo, usuario no repetido, contraseña segura).
- **`presentacion/`** solo pide datos y muestra resultados; toda la lógica la delega a la capa de negocio.
- **`auxiliares/`** reúne lo que usan varias capas: validaciones, constantes (`constantes.py`), mensajes reutilizables (`mensajes.py`), formatos, cálculos, seguridad (`seguridad.py`) y registro de errores.

### Repositorios con funciones
Cada entidad tiene su repositorio en `datos/repositorio/` hecho con **funciones** (no con clases). Por ejemplo, `repositorio_docentes.py`:
```python
def guardar(docente):          # inserta o actualiza con save()
def listar():                  # todos los docentes
def obtener_por_id(id_docente):
def buscar(texto):             # búsqueda por nombre
def eliminar(docente):
```
Las funciones genéricas que comparten todos (manejo de errores, listar, buscar, revisar repetidos) están en `repositorio_base.py`.

## Principios de POO aplicados
| Principio | Dónde se aplica |
|---|---|
| **Abstracción** | `NegocioBase`, `MenuBase` y `MenuCrud` son clases abstractas (`ABC`): definen *qué* se puede hacer y ocultan el *cómo*. La clase `Conexion` oculta los detalles de MySQL. |
| **Encapsulamiento** | Atributos privados (`__repositorio`, `__negocio`, `__base_datos`, `__titulo`, `__usuario_sesion`) a los que solo se accede con propiedades de lectura (`@property`). |
| **Herencia** | `Persona` → `Estudiante`, `Docente` y `Apoderado`. `ModelBase` → todos los modelos. Cada clase de negocio y cada menú hereda de su clase base, y así no se repite el CRUD 11 veces. |
| **Polimorfismo** | Cada modelo implementa a su manera `columnas()`, `fila()` y `mostrar_datos()`, y una misma función muestra cualquier modelo en una tabla. `NegocioEstudiantes` y `NegocioUsuarios` redefinen `eliminar()` para hacer una eliminación lógica (desactivar en vez de borrar). El menú principal trata igual a los 10 submenús. |

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
SOURCE datos/sql/2026.11.27_10.00_ddl_usuarios.sql;
SOURCE datos/sql/2026.11.27_10.15_Insert_Usuario_Inicial.sql;
```
> **¿Ya tenían la base de datos de la Evaluación 2?** No hay que borrarla: basta con ejecutar solo los dos últimos scripts (tabla `usuarios` y usuario inicial).

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

## Usuario inicial
El script `2026.11.27_10.15_Insert_Usuario_Inicial.sql` crea el primer usuario para poder entrar:

| Usuario | Contraseña |
|---|---|
| `admin` | `Admin2026!` |

En la base de datos no está la contraseña, sino su **hash BCrypt** (`$2b$12$...`).
**Después del primer ingreso, cambie esta contraseña** en el menú *Usuarios → Cambiar contraseña*.

## Seguridad y login
- **Maskpass**: al escribir la contraseña se ven asteriscos (`****`) en vez de lo que se escribe.
- **BCrypt** (costo 12): la contraseña se guarda como hash con sal aleatoria. Ni siquiera nosotros podemos leerla desde la base de datos.
- Mismo mensaje si el usuario no existe o si la contraseña está mala ("Usuario o contraseña incorrectos"), para no dar pistas sobre qué usuarios existen.
- Máximo **3 intentos** de login; después la aplicación se cierra.
- Los usuarios no se borran, se **deshabilitan** (ya no pueden entrar). No se puede deshabilitar el usuario con el que se inició sesión.
- Contraseñas de al menos 8 caracteres, con letras y números. Para cambiar la propia contraseña se pide la actual.

---

## Control de dependencias (`requirements.txt`)
Para instalar todas las librerías necesarias (Peewee, PyMySQL, BCrypt, Maskpass, PrettyTable, python-decouple, pytest y cryptography), ejecutamos en la terminal:
```bash
pip install -r requirements.txt
```

## Ejecución y pruebas
Para iniciar el sistema:
```bash
python main.py
```
Lo primero que aparece es el **inicio de sesión**: ingrese `admin` / `Admin2026!` (o su propio usuario).
> Ejecútelo desde una terminal (CMD, PowerShell o la terminal de Linux). Algunas consolas de los editores no funcionan bien con Maskpass al pedir la contraseña.
Para ejecutar las pruebas automáticas (usan una base de datos de prueba en memoria, así que no necesitan MySQL ni `.env`):
```bash
pytest
```
> **En Windows**, si `python` o `pip` no se reconocen, usamos `py main.py`, `py -m pip install -r requirements.txt` y `py -m pytest`.
