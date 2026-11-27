"""Constantes y configuración general de la aplicación.

Se reúnen aquí para no repetir "números mágicos" en el código:
si hay que cambiar uno, se cambia en un solo lugar.
"""

# ----- Aplicación -----
NOMBRE_APP = 'Sistema de Gestión Escolar - INACAP'
VERSION_APP = 'v3.0'
AUTORES = 'Cristopher Alexis Lagos Ancan, Alexander Bombin Figueroa'
MODULO = 'Programación Orientada a Objetos - INACAP'

# ----- Login y contraseñas -----
MAX_INTENTOS_LOGIN = 3          # después de 3 intentos fallidos se cierra la aplicación
LARGO_MINIMO_CLAVE = 8
LARGO_MAXIMO_CLAVE_BYTES = 72   # BCrypt solo usa los primeros 72 bytes de la contraseña
COSTO_BCRYPT = 12               # mientras más alto, más lento (y difícil de atacar) es el hash
CARACTER_MASCARA = '*'          # carácter que muestra maskpass al escribir la contraseña

# ----- Usuarios -----
LARGO_MINIMO_USUARIO = 4
LARGO_MAXIMO_USUARIO = 30
