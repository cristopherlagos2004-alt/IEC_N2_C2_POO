"""Hash de contraseñas con PBKDF2-HMAC-SHA256 (solo librería estándar de Python).

¿Por qué hash y no cifrado?
- Un CIFRADO se puede revertir con una llave: si alguien roba la llave, obtiene
  todas las contraseñas.
- Un HASH no se puede revertir. Para revisar una contraseña se vuelve a calcular
  el hash de lo que escribió el usuario y se compara con el guardado.

¿Por qué PBKDF2 y no un simple SHA-256?
- SHA-256 es muy rápido: un atacante puede probar miles de millones de
  contraseñas por segundo. PBKDF2 repite el cálculo cientos de miles de veces
  (ITERACIONES), así cada intento le cuesta mucho más.
- La SAL es un valor aleatorio distinto para cada usuario. Así, dos usuarios con
  la misma contraseña tienen hashes distintos y no sirven tablas precalculadas.

Formato guardado en la base de datos (un solo texto):
    pbkdf2_sha256$600000$<sal en base64>$<hash en base64>
Guardar el algoritmo y las iteraciones permite subirlas en el futuro sin
romper las contraseñas que ya existen.
"""
import base64
import hashlib
import hmac
import secrets

ALGORITMO = 'pbkdf2_sha256'
ITERACIONES = 600_000  # valor recomendado por OWASP (2023) para PBKDF2-HMAC-SHA256
LARGO_SAL = 16         # bytes


def _calcular(contrasena: str, sal: bytes, iteraciones: int) -> bytes:
    return hashlib.pbkdf2_hmac('sha256', contrasena.encode('utf-8'), sal, iteraciones)


def generar_hash(contrasena: str) -> str:
    """Devuelve el texto que se guarda en la base de datos (nunca la contraseña)."""
    sal = secrets.token_bytes(LARGO_SAL)  # secrets: aleatorio seguro (random no lo es)
    resumen = _calcular(contrasena, sal, ITERACIONES)
    return '$'.join([ALGORITMO, str(ITERACIONES),
                     base64.b64encode(sal).decode('ascii'),
                     base64.b64encode(resumen).decode('ascii')])


def verificar_contrasena(contrasena: str, hash_guardado: str) -> bool:
    """True si la contraseña corresponde al hash guardado.

    Si el hash guardado está dañado o tiene otro formato, devuelve False
    (no lanza error, para no dar pistas a quien intenta entrar).
    """
    try:
        algoritmo, iteraciones, sal_b64, resumen_b64 = hash_guardado.split('$')
        if algoritmo != ALGORITMO:
            return False
        sal = base64.b64decode(sal_b64, validate=True)
        esperado = base64.b64decode(resumen_b64, validate=True)
        calculado = _calcular(contrasena, sal, int(iteraciones))
    except (ValueError, AttributeError, TypeError):
        return False
    # compare_digest tarda lo mismo aunque los textos difieran al principio,
    # así no se puede adivinar el hash midiendo cuánto demora la comparación.
    return hmac.compare_digest(calculado, esperado)


_hash_falso = None


def hash_falso() -> str:
    """Hash de una contraseña al azar que nadie conoce.

    Se usa cuando el usuario no existe, para que el login tarde lo mismo que con
    un usuario real (si respondiera más rápido, un atacante sabría qué usuarios
    existen). Se calcula una sola vez y solo cuando se necesita, para no hacer
    lento el inicio del programa.
    """
    global _hash_falso
    if _hash_falso is None:
        _hash_falso = generar_hash(secrets.token_urlsafe(16))
    return _hash_falso
