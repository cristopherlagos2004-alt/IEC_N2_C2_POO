# Sistema de Gestión Escolar - POO INACAP
Desarrollo de Proyecto de Programación Orientada a Objetos
Alumnos: Cristopher Alexis Lagos Ancan, Alexander Bombin Figueroa
Carrera: Ingeniería / Ciberseguridad - INACAP (Segundo Semestre 2026)

---

## Descripción del Proyecto
Este proyecto está diseñado siguiendo una **arquitectura por capas** (Datos, Negocio y Presentación), aplicando Programación Orientada a Objetos en Python y conectándose a una base de datos MySQL mediante el ORM Peewee. Está basado en nuestro diagrama UML de Gestión Escolar (`diagrama/ev1poo.drawio`), que incluye las entidades Estudiante, Curso, Docente, Asignatura, Evaluación, Apoderado, Asistencia, Calificación, Pago y Periodo Académico.

## Estructura Modular
El desarrollo modular nos ayuda a mantener el código ordenado en partes más pequeñas e independientes:
- **`datos/`**: la conexión (`conexion.py`), la configuración (`auxiliar.py`), un modelo por entidad en `modelos/`, los repositorios con las consultas ORM en `repositorio/` y los scripts SQL en `sql/`, ordenados por fecha.
- **`negocio/`**: maneja la lógica de las operaciones, valida los datos (`validaciones.py`: RUT, nombre y fecha) y da formato a los resultados con `PrettyTable`.
- **`presentacion/`**: contiene los menús interactivos por consola y la interacción con el usuario mediante `input()`. Solo se comunica con la capa de negocio.
- **`tests/`**: pruebas automáticas de las validaciones.

---

## Control de Base de Datos y Configuración
Para conectarnos a la base de datos desde nuestra aplicación usamos el ORM *Peewee* y el driver *PyMySQL*.

### 1. Crear la base de datos
Ejecutamos los scripts de `datos/sql/` **en orden de fecha** (el nombre de cada archivo indica su orden):

1. `2026.09.11_09.40_ddl_gestion_escolar.sql`: crea la base `gestion_escolar` y sus tablas.
2. Los scripts `Insert_*` y `Alter_*`, en el orden en que aparecen.

> Si la base ya estaba creada con la versión anterior (tabla `periodicos_academicos`), primero la borramos con `DROP DATABASE gestion_escolar;` y luego ejecutamos todos los scripts de nuevo.

### 2. Crear el usuario de la aplicación
Para crear el usuario y otorgarle privilegios en MySQL, ejecutamos como `root` el script `2026.10.18_20.00_Usuario_Aplicacion.sql`:
```sql
CREATE USER IF NOT EXISTS 'usuario_escolar'@'localhost'
    IDENTIFIED WITH caching_sha2_password BY 'cambiar_esta_contraseña';
GRANT SELECT, INSERT, UPDATE, DELETE ON gestion_escolar.* TO 'usuario_escolar'@'localhost';
FLUSH PRIVILEGES;
```
Le damos solo **los privilegios mínimos** que la aplicación necesita (leer, insertar, modificar y eliminar datos). No usamos `ALL PRIVILEGES`, porque eso permitiría borrar tablas o cambiar la estructura de la base.

> Cada integrante reemplaza `cambiar_esta_contraseña` por su propia contraseña **al ejecutar el script en su equipo**. La contraseña real no se guarda en el repositorio.

### 3. Configurar la conexión (`.env`)
Copiamos el archivo `.env.example` con el nombre `.env` y completamos los datos de conexión:
```
DB_NAME=gestion_escolar
DB_HOST=localhost
DB_PORT=3306
DB_USER=usuario_escolar
DB_PASSWORD=tu_contraseña
```
El archivo `.env` está incluido en `.gitignore`, así que **nunca se sube a GitHub**.

---

## Control de dependencias (`requirements.txt`)
Para instalar todas las librerías necesarias de forma automática (Peewee, PyMySQL, PrettyTable, python-decouple, pytest y cryptography), ejecutamos en la terminal de VS Code:
```bash
pip install -r requirements.txt
```

---

## Ejecución y pruebas
Para iniciar el sistema:
```bash
python main.py
```
Para ejecutar las pruebas automáticas:
```bash
pytest
```
