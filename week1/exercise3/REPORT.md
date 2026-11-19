# Informe — Ejercicio 3: Un modelo en tu propia máquina

**Modelo:** `ministral-3:8b` (~6 GB, 4-bit) con Ollama 0.40.14.
**Máquina:** 15 GB de RAM, NVIDIA RTX 2060 con 6 GB de VRAM (el modelo se reparte ~85 % GPU / ~15 % CPU). Elegí el 8B porque el 14B (~9 GB) no cabe en la GPU.
**Método:** cada prueba se hizo en una conversación nueva, sin historial (`run_tests.py`, respuestas completas en `results.json`). Con muestreo, otra ejecución puede dar respuestas distintas.

## Qué pudo hacer bien
- **Tarea en lenguaje natural, sin ejemplos:** explicó por qué el cielo es azul en dos frases claras y adaptadas a un niño de 10 años (17 s).
- **Otro idioma:** en catalán respondió correcto y natural, en tres líneas como se pedía.
- **JSON estricto:** los datos son correctos (`Japón`, `Tokio`, `125000000`) y el JSON es válido (9 s). Ver el matiz más abajo.
- **Código:** escribió una función Python limpia, con docstring, explicación y tests (84 s).

## Qué me sorprendió
- **Lo bien que suena todo, incluso lo equivocado.** El tono es igual de seguro cuando acierta que cuando inventa.
- **El libro inventado.** Se le pidió el argumento de un libro que no existe (*La biblioteca de cristal de Anselmo Ferrán*, 2011) y no dudó: inventó la trama, los personajes (Javier y Lucía), el simbolismo y hasta un «primer párrafo» literal. Pidió detalles al final como si lo conociera.
- **La velocidad desigual.** Las respuestas cortas tardan 3–9 s, pero la prueba de la regla inventada tardó 122 s porque escribió una respuesta enorme y dubitativa.
- **El modelo describe una regla que sus propias respuestas incumplen** (ver prueba 2).

## Dónde falló o se equivocó con seguridad

| Prueba | Qué pasó | Correcto |
|---|---|---|
| **Letras en «strawberry»** | «hay **2** letras r» (sin dudar) | 3 |
| **Multiplicación 48217 × 3906** | `18,768,607,22` (ni siquiera es un número bien formado) | 188335602 |
| **Libro inexistente** | Resumen y primer párrafo inventados, sin avisar | Debió decir que no lo conoce |
| **Regla inventada (invertir letras)** | Ver abajo | `gato → otag` |
| **Código (palíndromo)** | Dijo que ambos tests pasaban, pero el primero falla | Ver abajo |
| **JSON «sin markdown»** | Lo envolvió en un bloque ```` ```json ```` | Solo el JSON, sin bloque |

### Regla inventada (few-shot)
La regla era invertir las letras (`sol → los`, `mar → ram`).

- **Primer intento:** tuve un error mío: escribí `luna -> aunl` en vez de `luna -> anul`. Con ese ejemplo incoherente el modelo se perdió en una respuesta larguísima, probó varias reglas y acabó en `gato → tago`.
- **Intento corregido** (`results_test2_corregido.json`, ejemplo `luna -> anul`): sigue fallando. Afirma que la regla es «mover la primera letra al final» y responde `atog`. Esa regla daría `luna → unal`, no `anul`, así que su explicación no cuadra con los propios ejemplos. El resultado correcto es `otag`.
- Es decir: con 3 ejemplos de una regla simple, un modelo de 8B no la dedujo, y justificó su respuesta con una regla que no encaja.

### Código con test que falla
La función `es_palindromo` solo elimina espacios (`''.join(cadena.split()).lower()`), no la puntuación. El primer test del propio modelo, `"A man, a plan, a canal: Panama"`, devuelve `False` (lo comprobé ejecutándolo), pero él afirma «ambos tests pasan». El código es razonable para el enunciado (ignorar espacios y mayúsculas), pero el test que eligió no lo cumple, y no lo ejecutó para verlo.

## ¿Cambian los resultados entre conversaciones?
Cada prueba fue una conversación nueva. Solo repetí la prueba de la regla, y la segunda respuesta fue distinta de la primera (distinta respuesta, ambas incorrectas). Con temperatura > 0 las respuestas varían, así que conviene no fiarse de una sola ejecución.

## Conclusión
El modelo es muy útil para tareas de lenguaje (explicar, traducir, dar formato, escribir código tipo plantilla), y corre en un portátil con una GPU modesta. Pero no sabe cuándo no sabe: falla con seguridad en tareas que requieren contar, calcular o ejecutar algo mecánicamente (letras, multiplicaciones, tests), y alucina contenido sobre cosas inexistentes. Es una buena razón para verificar siempre lo que dice, y para darle herramientas (calculadora, intérprete de código, búsqueda) en lugar de confiar solo en el modelo.
