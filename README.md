# Sistema de Gestión Escolar - POO INACAP

**Desarrollo de Proyecto de Programación Orientada a Objetos**

- **Alumnos:** Cristopher Alexis Lagos Ancan, Alexander Bombin Figueroa
- **Carrera:** Ingeniería / Ciberseguridad - INACAP (Segundo Semestre 2026)

---

## Descripción del Proyecto
Sistema de consola para gestionar un colegio. Está diseñado con una **arquitectura por capas** (Datos, Negocio y Presentación), aplicando Programación Orientada a Objetos en Python y conectándose a una base de datos MySQL mediante el ORM Peewee.

Está basado en nuestro diagrama de clases UML (`ev1poo.drawio`, en la raíz del proyecto), que incluye las entidades Persona, Estudiante, Docente, Apoderado, Curso, Asignatura, Evaluación, Calificación, Asistencia, Pago, Periodo Académico y Usuario.

Desde el menú principal se puede navegar por los 10 componentes del sistema, más **Usuarios**, y hacer en cada uno las operaciones **CRUD**: listar, registrar, buscar, actualizar y eliminar.

## Estructura Modular
```
IEC_N2_C2_POO/
├── main.py              ← inicia la aplicación (primero pide iniciar sesión)
├── crear_usuario.py     ← crea el primer usuario del sistema
├── ev1poo.drawio        ← diagrama de clases UML
├── auxiliares/          ← validaciones, formatos, cálculos, errores y hash bcrypt (seguridad.py)
├── datos/               ← capa de datos
│   ├── conexion.py      ← clase Conexion (conexión a MySQL)
│   ├── modelos/         ← una clase por entidad del UML
│   ├── repositorio/     ← persistencia y acceso a la información (CRUD con Peewee)
│   ├── sql/             ← scripts para crear y mantener la base de datos
│   └── servicios/       ← consumo de APIs externas (Evaluación 3)
├── negocio/             ← reglas de negocio de cada entidad
├── presentacion/        ← menús de consola
└── tests/               ← pruebas automáticas
```
- **`auxiliares/`** tiene funciones de apoyo que usan varias capas (validar un RUT, dar formato a un monto, calcular un hash, registrar errores). No guarda datos ni conoce la base de datos, por eso está fuera de `datos/`.
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

## Instalación y puesta en marcha (paso a paso)

### 1. Dependencias (`requirements.txt`)
Todas las librerías tienen la versión fija, para que el programa funcione igual en todos los equipos:

| Librería | Para qué |
|---|---|
| `peewee` | ORM: las tablas se manejan como clases de Python |
| `PyMySQL` + `cryptography` | driver de MySQL (`cryptography` es necesaria para el método de autenticación `caching_sha2_password` de MySQL 8) |
| `python-decouple` | lee las credenciales desde el archivo `.env` |
| `prettytable` | tablas en la consola |
| `requests` | consumo de las APIs externas |
| **`bcrypt`** | hash de las contraseñas (Evaluación 3) |
| **`maskpass`** | escribir la contraseña mostrando `*` (Evaluación 3) |
| `pytest` | pruebas automáticas |

Creamos un entorno virtual (así no se mezclan con las librerías del sistema) e instalamos:
```bash
cd ~/IEC_N2_C2_POO
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
> **Windows:** `py -m venv .venv`, luego `.venv\Scripts\activate` y `py -m pip install -r requirements.txt`.
>
> **Linux:** `maskpass` instala `pynput`, que a su vez compila `evdev`. Si `pip` muestra un error de compilación, instalamos primero las herramientas: `sudo apt install build-essential python3-dev` y repetimos el `pip install`.
>
> Nunca usamos `pip install --break-system-packages`: todo se instala dentro del `.venv`.

### 2. Crear la base de datos
Entramos a MySQL como `root` **desde la carpeta del proyecto** (así funcionan las rutas de `SOURCE`):
```bash
cd ~/IEC_N2_C2_POO
mysql -u root -p --default-character-set=utf8mb4
```
> En Windows, la opción `--default-character-set=utf8mb4` es necesaria. Sin ella, la ñ y los tildes de los datos de prueba se guardan mal.

Ejecutamos **todos** los scripts de `datos/sql/` **en orden de fecha** (el nombre de cada archivo indica su orden):
```sql
SOURCE datos/sql/2026.09.11_09.40_ddl_gestion_escolar.sql;
SOURCE datos/sql/2026.09.11_10.30_Insert_Periodos.sql;
SOURCE datos/sql/2026.09.11_10.45_Insert_Cursos.sql;
SOURCE datos/sql/2026.09.14_11.05_Insert_Docentes.sql;
SOURCE datos/sql/2026.09.21_10.30_Insert_Estudiantes.sql;
SOURCE datos/sql/2026.10.09_09.45_Alter_Estudiantes.sql;
SOURCE datos/sql/2026.10.16_10.10_Alter_Asistencias.sql;
-- 2026.10.18_20.00_Usuario_Aplicacion.sql: NO se ejecuta con SOURCE (ver paso 3)
SOURCE datos/sql/2026.11.20_10.00_Tabla_Usuarios.sql;
```
> Si la base ya estaba creada con la versión anterior (tabla `periodicos_academicos`), primero la borramos con `DROP DATABASE gestion_escolar;` y luego ejecutamos todos los scripts de nuevo.

### 3. Crear el usuario de MySQL de la aplicación
El script `2026.10.18_20.00_Usuario_Aplicacion.sql` muestra cómo crear el usuario. **No editamos ese archivo**, para que la contraseña no termine en GitHub. En su lugar, copiamos estos comandos en MySQL (todavía como `root`) poniendo nuestra propia contraseña:
```sql
CREATE USER IF NOT EXISTS 'usuario_escolar'@'localhost'
    IDENTIFIED WITH caching_sha2_password BY 'cambiar_esta_contraseña';
GRANT SELECT, INSERT, UPDATE, DELETE ON gestion_escolar.* TO 'usuario_escolar'@'localhost';
FLUSH PRIVILEGES;
```
Le damos solo **los privilegios mínimos** que la aplicación necesita (leer, insertar, modificar y eliminar datos). No usamos `ALL PRIVILEGES`, porque eso permitiría borrar tablas o cambiar la estructura de la base. Salimos de MySQL con `exit`.

### 4. Configurar la conexión (`.env`)
Copiamos `.env.example` con el nombre `.env` (`cp .env.example .env`) y completamos los datos:
```
DB_NAME=gestion_escolar
DB_HOST=localhost
DB_PORT=3306
DB_USER=usuario_escolar
DB_PASSWORD=tu_contraseña
OPENWEATHER_API_KEY=tu_llave_de_openweathermap
```
El archivo `.env` está incluido en `.gitignore`, así que **nunca se sube a GitHub**. La llave de OpenWeatherMap se obtiene gratis en su página y puede demorar hasta 2 horas en activarse.

### 5. Crear el primer usuario del sistema
```bash
python3 crear_usuario.py
```
Pide el nombre de usuario y la contraseña dos veces (se ven `*` al escribirla). En la base solo se guarda el **hash bcrypt**. Este script **solo funciona si todavía no hay usuarios**: los demás se crean desde el menú **Usuarios**, con la sesión iniciada.

Reglas de la contraseña: al menos 8 caracteres y como máximo **72 bytes** (límite de bcrypt; la ñ y cada tilde cuentan doble), con letras y números, sin caracteres de control y sin contener el nombre de usuario.

### 6. Ejecutar
```bash
python3 main.py
```
Lo primero que aparece es el **inicio de sesión**: sin iniciar sesión no se llega al menú.

### 7. Pruebas
```bash
python3 -m pytest
```
Usan una base de datos SQLite en memoria, así que no necesitan MySQL, `.env` ni internet. bcrypt usa costo 4 en las pruebas (para que corran rápido) y costo 12 en el programa.

> **En Windows**, si `python3` no se reconoce, usamos `py main.py`, `py crear_usuario.py` y `py -m pytest`.

---

## Evaluación 3: servicios externos y seguridad
El sistema ahora consume dos APIs externas con la librería oficial **requests**, y solo se puede usar después de **iniciar sesión**.

| API | Para qué la usa el colegio | Llave |
|---|---|---|
| [mindicador.cl](https://mindicador.cl) | UF, dólar, euro y UTM del día: cobrar mensualidades en UF y ver los pagos en otras monedas | No necesita |
| [OpenWeatherMap](https://openweathermap.org/current) | Clima actual para decidir si una clase de educación física o una salida se hace al aire libre | Sí (`OPENWEATHER_API_KEY` en el `.env`) |

La puesta en marcha completa está en **Instalación y puesta en marcha** (arriba).

### Gestión de usuarios (menú "Usuarios")
| Opción | Qué hace |
|---|---|
| Listar | muestra Id, usuario y si está bloqueado (**nunca el hash**) |
| Registrar | pide el nombre (avisa al tiro si ya existe) y la contraseña dos veces con `maskpass`; guarda solo el hash bcrypt |
| Buscar | busca por parte del nombre de usuario |
| Actualizar | cambia el nombre y, si se responde `s`, la contraseña (se guarda siempre como hash y se quita el bloqueo por intentos) |
| Eliminar | no deja eliminar al usuario con la sesión iniciada ni al último usuario |

Sigue el mismo patrón que las otras entidades: `RepositorioUsuarios` (hereda de `RepositorioBase`) → `NegocioUsuarios` (hereda de `NegocioBase`) → `MenuUsuarios` (hereda de `MenuCrud`). Todas sus operaciones exigen la sesión (`Sesion.exigir()`).

### Si ya tenía usuarios de la versión con PBKDF2
Un hash no se puede "convertir" a bcrypt, porque para eso habría que conocer la contraseña. Los usuarios antiguos **ya no pueden entrar** (el login responde "Usuario o contraseña incorrectos"). Para recrearlos:
```bash
mysql -u root -p -e "DELETE FROM gestion_escolar.usuarios;"
python3 crear_usuario.py
```
Luego se inicia sesión con ese usuario y se crean los demás desde el menú **Usuarios**.

### Dónde está cada cosa
```
datos/servicios/           ← NUEVO: consumo de APIs
│   ├── cliente_http.py         requests con timeout, reintentos y revisión de códigos HTTP
│   ├── servicio_indicadores.py mindicador.cl (UF, dólar, euro, UTM)
│   ├── servicio_clima.py       OpenWeatherMap
│   ├── cache_local.py          último valor válido en datos/cache/indicadores.json
│   └── errores_servicio.py     jerarquía de excepciones y registro sin llaves
auxiliares/seguridad.py         hash de contraseñas con bcrypt (hashpw / checkpw, costo 12)
datos/modelos/usuario.py        tabla usuarios
negocio/negocio_autenticacion.py  login, bloqueo por intentos y clase Sesion
negocio/negocio_usuarios.py       reglas de la gestión de usuarios
negocio/negocio_servicios.py      conversiones de moneda y recomendación según el clima
presentacion/presentacion_login.py      pantalla de inicio de sesión
presentacion/presentacion_servicios.py  menú "Servicios externos"
presentacion/presentacion_usuarios.py   menú "Usuarios"
presentacion/consola.py                 pedir_contrasena(): único lugar donde se lee una contraseña (maskpass)
crear_usuario.py                script para crear el primer usuario
BITACORA_IA.md                  uso de IA: prompts, problemas encontrados y ajustes
```

### Medidas de seguridad
- **Contraseñas:** solo se guarda su hash **bcrypt** (`bcrypt.hashpw` con sal aleatoria y costo 12); se comparan con `bcrypt.checkpw`, que tarda lo mismo aunque difieran al principio. Se rechazan las de más de 72 bytes (bcrypt ignoraría el resto) y las que tienen caracteres de control (bcrypt corta en el byte nulo). Al escribirla se ve un `*` por carácter (`maskpass.askpass(mask="*")`), en el login, en el menú Usuarios y en `crear_usuario.py`.
- **Login:** el mismo mensaje si el usuario no existe o si la clave está mal; la cuenta se bloquea 5 minutos tras 3 intentos fallidos.
- **Acceso:** sin sesión no se llega al menú, y además cada función que consume una API o gestiona usuarios exige la sesión (`Sesion.exigir()`). No se puede eliminar al usuario de la sesión ni dejar el sistema sin usuarios.
- **Arquitectura:** la capa de presentación no importa nada de `datos/`; lo revisa la prueba `tests/test_arquitectura.py`.
- **Entradas:** ciudad, país, moneda, montos y credenciales se validan antes de llamar a la API. La moneda se revisa contra una lista blanca.
- **Secretos:** la llave de la API y la contraseña de MySQL están en el `.env` (fuera de GitHub). Si un error trae la URL con la llave, se oculta (`appid=***`) antes de guardarlo en `errores.log`.
- **Errores:** `timeout` en todas las solicitudes, un reintento ante fallas pasajeras, un error distinto por cada código HTTP, y mensajes para el usuario sin detalles técnicos. Si mindicador.cl no responde, se usa el último valor guardado y se avisa de qué fecha es.
