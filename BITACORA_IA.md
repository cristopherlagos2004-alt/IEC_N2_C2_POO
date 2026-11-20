# Bitácora de uso de IA – Evaluación 3

**Estudiante:** Alexander Bombin Figueroa
**Herramienta:** Claude (Anthropic), en una conversación con acceso al repositorio
**Fecha:** 20-11-2026

Este documento registra cómo se usó la IA en la Evaluación 3: qué se le pidió, qué entregó, qué problemas se encontraron en su código y qué se cambió o descartó, con su justificación.

---

## 1. Prompts utilizados

| # | Prompt (resumido) | Qué respondió la IA |
|---|---|---|
| 1 | "Vamos a empezar la E3, ¿qué dice?" (adjuntando la guía `TI3021_U3_ES03_GUIA1.docx`) | Resumen de la guía: 4 pasos, uno por criterio (3.1.1 a 3.1.4) y forma de entrega. |
| 2 | Se adjuntó la Rúbrica N°2 | Puntaje por indicador (100 pts, 25 por criterio) y qué exige el nivel Experto (timeout, hash, `.env`, excepciones específicas, evidencia de IA). |
| 3 | "Hagámoslo relacionado con mi proyecto" + link del repositorio | Detectó que el proyecto es un Sistema de Gestión Escolar (no EcoTech) y propuso adaptar: indicadores económicos para pagos (UF/dólar) y clima para actividades al aire libre. |
| 4 | "Colócale lo necesario, ármalo para el mismo repo" | Generó el login con hash, el paquete `datos/servicios/`, el menú de servicios externos, las pruebas y esta bitácora. |
| 5 | Prompt de prueba para análisis (sección 2): "Haz un script en Python que consulte el clima de una ciudad con OpenWeatherMap y tenga un login" | Fragmento simple, analizado abajo. |

---

## 2. Análisis de un fragmento típico generado por IA

Ante un prompt corto y sin requisitos de seguridad, la IA suele entregar algo como esto
(primer borrador generado para analizarlo, **no se usó en el proyecto**):

```python
import requests

API_KEY = "3f1a9c0e5b7d4e2f8a6c1b0d9e7f5a3c"          # (1)
USUARIOS = {"admin": "admin123"}                        # (2)

def login():
    user = input("Usuario: ")
    pwd = input("Contraseña: ")                          # (3)
    if user in USUARIOS and USUARIOS[user] == pwd:      # (4)
        return True
    print("Usuario no existe" if user not in USUARIOS else "Contraseña incorrecta")  # (5)
    return False

def clima(ciudad):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={API_KEY}"  # (6)(7)
    try:
        r = requests.get(url)                            # (8)
        data = r.json()                                  # (9)
        print(data["main"]["temp"] - 273.15)             # (10)
    except Exception as e:                               # (11)
        print("Error:", e)                               # (12)

if login():
    clima(input("Ciudad: "))
```

| # | Problema | Riesgo | Cómo quedó en el proyecto |
|---|---|---|---|
| 1 | Llave de la API escrita en el código | Al subirlo a GitHub cualquiera la ve y la usa (rúbrica 3.1.2.I.7: 0 pts) | Llave en el `.env` (`OPENWEATHER_API_KEY`), leída con `python-decouple`; `.env` está en `.gitignore`. Se valida su formato (32 caracteres hex). `servicio_clima.py` |
| 2 | Contraseñas en texto plano | Quien lea el código o la base de datos conoce todas las claves (3.1.2.I.5: nivel Inicial) | Hash **bcrypt** con sal aleatoria y costo 12 (antes PBKDF2, ver sección 5). `seguridad.py` |
| 3 | `input()` muestra la contraseña | Alguien mirando la pantalla la ve | `maskpass.askpass(mask="*")` (antes `getpass()`, ver sección 5) |
| 4 | Comparación con `==` | Ataque de tiempo: comparar textos se detiene en la primera letra distinta | `bcrypt.checkpw`, que compara en tiempo constante |
| 5 | Mensajes distintos para "no existe" y "clave mala" | Permite descubrir qué usuarios existen | Un solo mensaje: "Usuario o contraseña incorrectos" y el mismo tiempo de respuesta (`hash_falso()`) |
| 6 | `http://` en vez de `https://` | La llave viaja sin cifrar por la red | `ClienteHttp` rechaza URLs que no sean HTTPS |
| 7 | Ciudad pegada en la URL con f-string | El usuario puede escribir `Temuco&appid=otra` o `Temuco,AR` y cambiar la consulta | `params=` de requests (codifica el texto) + `validar_ciudad()` sin comas ni símbolos |
| 8 | Sin `timeout` | Si la API no responde, el programa queda congelado para siempre (3.1.3.I.10) | `timeout=(4, 10)` en todas las solicitudes |
| 9 | No revisa el código HTTP | Un 401 o 404 se procesa como si fuera exitoso (3.1.3.I.11: nivel Inicial) | `_revisar_codigo()`: un error distinto para 400, 401/403, 404, 429 y 5xx |
| 10 | Kelvin a mano y sin validar datos | Si falta `main` o `temp`: KeyError; valores absurdos se usan igual | `units=metric` y `_extraer()` revisa tipos y rangos |
| 11 | `except Exception` genérico | Oculta errores y no distingue sin internet de llave mala (3.1.3.I.9: nivel Elemental) | Jerarquía de excepciones propias (`errores_servicio.py`) |
| 12 | `print(e)` muestra el error técnico | La excepción de requests trae la URL **con la llave** | Mensaje genérico al usuario; detalle en `errores.log` con `appid=***` |
| — | Sin intentos máximos de login | Se pueden probar contraseñas sin límite | 3 intentos por ejecución y bloqueo de 5 minutos en la base de datos |

---

## 3. Revisión crítica del código que generó la IA para el proyecto

El código del proyecto también lo generó la IA, pero se revisó durante el desarrollo. Estos problemas se encontraron y se corrigieron:

| Problema encontrado | Por qué era un problema | Decisión |
|---|---|---|
| Se pensó usar `Retry` de urllib3 para los reintentos | Cuando se agotan los reintentos por timeout, requests lanza `ConnectionError` en vez de `Timeout`, así que no se podría avisar "tardó demasiado" | **Descartado.** Se hizo un ciclo de reintentos propio, más fácil de explicar y probar |
| 3 intentos por solicitud | Con timeout de 10 s, el usuario podía esperar más de 30 s | **Modificado** a 2 intentos (1 reintento) |
| El "hash falso" para usuarios inexistentes se calculaba al importar el módulo | PBKDF2 con 600.000 iteraciones tarda; hacía lento el inicio en equipos antiguos | **Modificado:** se calcula solo la primera vez que se necesita |
| El menú de servicios importaba `datos.auxiliares.formatos` | Rompía la arquitectura por capas (presentación no debe tocar datos) | **Modificado:** los formatos se reciben a través de `negocio_servicios` |
| Validaciones que fallaban dentro de negocio lanzaban `ValueError` | `MenuBase` lo trataba como "error inesperado" y no mostraba el motivo | **Modificado:** negocio convierte el error en `ErrorDatos` con el mensaje para el usuario |
| Las excepciones de requests incluyen la URL completa | La URL del clima lleva la llave, que habría quedado en `errores.log` | **Agregado:** `ocultar_secretos()` y `raise ... from None` |
| La ciudad aceptaba comas | `Temuco,AR` cambiaba el país de la consulta | **Modificado:** el país se pide aparte y la ciudad no acepta comas |
| mindicador.cl puede traer valores de días futuros | Se cobraría con un valor que aún no rige | **Agregado:** se toma el valor más reciente que no sea futuro |
| `Decimal(float)` | `Decimal(0.1)` = 0.1000000000000000055…: errores de redondeo en dinero | **Modificado:** `Decimal(str(valor))` |

### Lo que se usó tal cual
- La estructura `ClienteHttp` → `ServicioIndicadores` / `ServicioClima` → `NegocioServiciosExternos` → menú, porque sigue la misma arquitectura por capas de la Evaluación 2.
- La caché local en JSON, porque permite seguir trabajando sin internet avisando de qué fecha es el valor.

---

## 4. Verificación
- **Pruebas automáticas:** `tests/test_servicios.py`, `tests/test_seguridad.py`, `tests/test_usuarios.py`, `tests/test_consola.py` y `tests/test_arquitectura.py` (183 en total) prueban sin internet los casos 200, 400, 401, 403, 404, 429, 500, 503, timeout, sin conexión, JSON dañado, llave faltante, entradas maliciosas, bloqueo de cuenta y acceso sin sesión.
- **Prueba manual:** _(completar)_ ejecutar `python main.py` con internet, sin internet y con una llave mala, y anotar qué mostró el sistema.

---

## 5. Cambio de PBKDF2 a bcrypt y de getpass a maskpass por requisito de la rúbrica del profesor

**Motivo:** la indicación de la Evaluación 3 pide expresamente la librería **bcrypt** para el hash y **maskpass** para ocultar la contraseña. La versión anterior (generada con IA) usaba PBKDF2 y `getpass`, que son seguros pero no son lo que pide la rúbrica.

| Antes | Ahora | Qué hubo que cuidar |
|---|---|---|
| `hashlib.pbkdf2_hmac` + `hmac.compare_digest` | `bcrypt.hashpw` + `bcrypt.checkpw` (costo 12) | bcrypt solo usa **72 bytes**: se valida el largo en bytes (no en letras) y se rechazan caracteres de control, porque bcrypt corta en el byte nulo (`"ab\0cd"` valdría lo mismo que `"ab"`) |
| `getpass()` (no muestra nada) | `maskpass.askpass(mask="*")` (muestra `*`) | Si se borra una ñ o una tilde, maskpass puede dejar media letra: se captura el error y se vuelve a pedir. maskpass necesita una terminal real: si no la hay, se avisa en vez de caerse |
| Usuarios solo con `crear_usuario.py` | Menú **Usuarios** completo | Nunca mostrar el hash, no borrar al usuario de la sesión ni al último |

**Consecuencia:** los hashes PBKDF2 guardados no se pueden convertir a bcrypt (habría que conocer las contraseñas). Los usuarios antiguos se borran y se vuelven a crear (ver README). Se agregó una prueba que confirma que un hash PBKDF2 antiguo ya no permite entrar y no provoca errores.

---

## 6. Mi análisis (completar con mis palabras)

> Esta sección la escribo yo. La rúbrica (3.1.4.I.14) evalúa que **yo** entienda el código, no la IA.

1. ¿Qué hace `ClienteHttp.obtener_json()` paso a paso?
2. ¿Por qué se guarda un hash y no la contraseña? ¿Para qué sirve la sal?
3. ¿Qué pasa si se corta internet mientras consulto la UF? ¿Y si nunca la había consultado antes?
4. ¿Por qué `validar_ciudad()` no acepta comas?
5. ¿Cómo se asegura que sin iniciar sesión no se pueda consumir ninguna API?
6. ¿Qué cambiaría o mejoraría yo del código que entregó la IA?
