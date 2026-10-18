# Sistema de Gestión Escolar - POO INACAP
Desarrollo de Proyecto de Programación Orientada a Objetos 
Alumno: Cristopher Alexis Lagos Ancan
Carrera: Ingeniería / Cyberseguridad - INACAP (Segundo Semestre 2026)

---

## Descripción del Proyecto
Este proyecto está diseñado siguiendo una **arquitectura por capas** (Datos, Negocio y Presentación), aplicando Programación Orientada a Objetos en Python y conectándose a una base de datos MySQL mediante el ORM Peewee. Está basado en nuestro diagrama UML de Gestión Escolar (que incluye entidades como Estudiantes, Cursos, Docentes, Asignaturas, Evaluaciones, Apoderados, Asistencias, Calificaciones, Pagos y Periódicos Académicos).

## Estructura Modular
El desarrollo modular nos ayuda a mantener el código ordenado en partes más pequeñas e independientes:
- **`datos/`**: Contiene la conexión, los modelos unificados (`models.py`), los repositorios con las consultas ORM y los scripts SQL independientes ordenados por fechas.
- **`negocio/`**: Maneja la lógica de las operaciones y da formato a los resultados utilizando `PrettyTable`.
- **`presentacion/`**: Contiene los menús interactivos por consola y la interacción con el usuario mediante `input()`.

---

## Control de Base de Datos y Configuración
Para conectarnos a la base de datos desde nuestra aplicación usamos el ORM *Peewee* y el driver *PyMySQL*. 

Si necesitamos crear el usuario y otorgar privilegios en MySQL para este proyecto escolar, ejecutamos:
```sql
CREATE USER 'usuario_escolar'@'localhost' IDENTIFIED WITH caching_sha2_password BY 'tu_contraseña';
GRANT ALL PRIVILEGES ON db_gestion_escolar.* TO 'usuario_escolar'@'localhost';
FLUSH PRIVILEGES;
```

---

## Control de dependencias (`requirements.txt`)
Para instalar todas las librerías necesarias de forma automática (incluyendo Peewee, PyMySQL, PrettyTable, decouple, etc.), ejecutamos en la terminal de VS Code:
```bash
pip install -r requirements.txt
```
