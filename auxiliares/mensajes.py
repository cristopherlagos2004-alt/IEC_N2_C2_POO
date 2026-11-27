"""Mensajes reutilizables que se muestran al usuario."""

# ----- Base de datos -----
MENSAJE_GENERAL = 'Ocurrió un error con la base de datos. Revise el archivo errores.log.'
MENSAJE_INTEGRIDAD = ('No se pudo completar la operación: el dato está repetido '
                      'o hay otros registros que dependen de este.')
MENSAJE_ERROR_INESPERADO = 'Ocurrió un error inesperado. Revise el archivo errores.log.'

# ----- Menús -----
OPCION_INVALIDA = 'Opción ingresada NO corresponde. Ingrese nuevamente.'
OPERACION_CANCELADA = 'Operación cancelada.'
SIN_REGISTROS = 'No hay registros.'
SIN_REGISTROS_PARA_MOSTRAR = 'No hay registros para mostrar.'
ID_NO_ENCONTRADO = 'No se encontró un registro con ese Id.'
SALIENDO = 'Saliendo del Sistema'

# ----- Login -----
# Mismo mensaje si el usuario no existe o si la contraseña está mala:
# así no se le da pistas a un atacante sobre qué usuarios existen.
LOGIN_TITULO = 'Inicio de sesión'
LOGIN_INCORRECTO = 'Usuario o contraseña incorrectos.'
LOGIN_BLOQUEADO = 'Se superó el número de intentos permitidos. La aplicación se cerrará.'
LOGIN_BIENVENIDA = 'Bienvenido(a), {nombre}.'
LOGIN_INTENTOS_RESTANTES = 'Le quedan {intentos} intento(s).'
LOGIN_SIN_USUARIOS = ('No hay usuarios activos en la base de datos. '
                      'Ejecute el script del usuario inicial (ver README.md).')

# ----- Contraseñas -----
CLAVES_NO_COINCIDEN = 'Las contraseñas no coinciden.'
