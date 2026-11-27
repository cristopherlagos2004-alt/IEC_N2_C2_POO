"""Protección de contraseñas con BCrypt.

Las contraseñas NUNCA se guardan en texto plano: se guarda su hash.
Un hash no se puede "deshacer" para obtener la contraseña; para revisar
un login se vuelve a calcular y se compara.

Ejemplo:
    hash = generar_hash('MiClave123')   # '$2b$12$Qx...' (60 caracteres, distinto cada vez)
    verificar_clave('MiClave123', hash) # True
    verificar_clave('otra', hash)       # False
"""
import bcrypt

from auxiliares.constantes import COSTO_BCRYPT

# Hash de una contraseña cualquiera. Se usa cuando el usuario NO existe, para que el
# login tarde lo mismo que con un usuario real (si respondiera más rápido, un atacante
# podría descubrir qué nombres de usuario existen midiendo el tiempo de respuesta).
_HASH_FALSO = bcrypt.hashpw(b'usuario-inexistente', bcrypt.gensalt(COSTO_BCRYPT))


def generar_hash(clave: str) -> str:
    """Devuelve el hash BCrypt de la contraseña (incluye una 'sal' aleatoria)."""
    return bcrypt.hashpw(clave.encode('utf-8'), bcrypt.gensalt(COSTO_BCRYPT)).decode('utf-8')


def verificar_clave(clave: str, hash_guardado: str | None) -> bool:
    """True si la contraseña corresponde al hash guardado."""
    if not hash_guardado:
        bcrypt.checkpw(clave.encode('utf-8'), _HASH_FALSO)  # gasta el mismo tiempo
        return False
    try:
        return bcrypt.checkpw(clave.encode('utf-8'), hash_guardado.encode('utf-8'))
    except ValueError:  # el valor guardado no es un hash BCrypt válido
        return False
