"""Hash de contraseñas con bcrypt (requisito de la Evaluación 3).

¿Por qué hash y no cifrado?
- Un CIFRADO se puede revertir con una llave: si alguien roba la llave, obtiene
  todas las contraseñas.
- Un HASH no se puede revertir. Para revisar una contraseña se vuelve a calcular
  el hash de lo que escribió el usuario y se compara con el guardado.

¿Por qué bcrypt y no un simple SHA-256?
- SHA-256 es muy rápido: un atacante puede probar miles de millones de
  contraseñas por segundo. bcrypt es lento A PROPÓSITO: el COSTO indica cuántas
  vueltas da (2^12 = 4096 con costo 12), así cada intento le cuesta mucho más.
- bcrypt genera una SAL aleatoria distinta para cada hash. Así, dos usuarios con
  la misma contraseña tienen hashes distintos y no sirven tablas precalculadas.

Formato guardado en la base de datos (60 caracteres, un solo texto):
    $2b$12$<sal de 22 caracteres><hash de 31 caracteres>
     |   |
     |   +-- costo (12)
     +------ versión del algoritmo
La sal y el costo van dentro del mismo texto, por eso checkpw() no necesita
que se los pasemos aparte.

Límite de 72 bytes: bcrypt solo usa los primeros 72 bytes de la contraseña.
La versión 5 de la librería lanza ValueError si se pasa de eso, así que se
valida antes (validaciones.validar_contrasena_ingresada) y aquí se revisa otra
vez por seguridad. Ojo: son BYTES, no letras: la ñ y las tildes ocupan 2.
"""
import secrets

import bcrypt

COSTO_PRODUCCION = 12    # ~0,3 s por hash en un MacBook Air 2015: lento para un atacante, aceptable para un login
COSTO = COSTO_PRODUCCION  # las pruebas lo bajan a 4 (el mínimo) para correr rápido; ver tests/conftest.py
LARGO_MAXIMO_BYTES = 72  # límite propio de bcrypt
CODIFICACION = 'utf-8'


def _a_bytes(contrasena: str) -> bytes:
    """bcrypt trabaja con bytes. Lanza ValueError si pasa de 72 bytes."""
    clave = contrasena.encode(CODIFICACION)
    if len(clave) > LARGO_MAXIMO_BYTES:
        raise ValueError(f'La contraseña no puede ocupar más de {LARGO_MAXIMO_BYTES} bytes.')
    return clave


def generar_hash(contrasena: str) -> str:
    """Devuelve el texto que se guarda en la base de datos (nunca la contraseña).

    bcrypt.gensalt() crea una sal aleatoria nueva y bcrypt.hashpw() calcula el hash.
    Se lee COSTO al momento de llamar (no al importar) para que las pruebas
    puedan usar un costo bajo y correr rápido.
    """
    resumen = bcrypt.hashpw(_a_bytes(contrasena), bcrypt.gensalt(rounds=COSTO))
    return resumen.decode('ascii')


def verificar_contrasena(contrasena: str, hash_guardado: str) -> bool:
    """True si la contraseña corresponde al hash guardado.

    bcrypt.checkpw() saca la sal y el costo del hash guardado, recalcula y
    compara en tiempo constante (no se puede adivinar midiendo cuánto tarda).
    Si el hash guardado está dañado o es de otro algoritmo (por ejemplo, un hash
    PBKDF2 de la versión anterior), devuelve False en vez de lanzar un error,
    para no dar pistas a quien intenta entrar.
    """
    try:
        return bcrypt.checkpw(_a_bytes(contrasena), hash_guardado.encode('ascii'))
    except (ValueError, AttributeError, TypeError):
        # ValueError incluye UnicodeError (texto raro) y "Invalid salt" (hash que no es bcrypt)
        return False


def es_hash_bcrypt(hash_guardado) -> bool:
    """True si el texto tiene la forma de un hash bcrypt ($2a$, $2b$ o $2y$, 60 caracteres)."""
    return (isinstance(hash_guardado, str) and len(hash_guardado) == 60
            and hash_guardado[:4] in ('$2a$', '$2b$', '$2y$'))


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
