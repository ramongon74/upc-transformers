# Informe — Ejercicio 4: Llamar al LLM desde código

## Modelo y máquina
- **Modelo:** `ministral-3:8b` (~6 GB, 4-bit), servido por Ollama 0.40.14 en `http://localhost:11434/v1`.
- **Máquina:** WSL2 (Linux 6.18) sobre un PC con 15 GB de RAM y NVIDIA RTX 2060 (6 GB de VRAM). Ollama reparte el modelo ~85 % GPU / ~15 % CPU.
- **Configuración:** `.env` copiado de `.env.example` sin cambios (`OPENAI_ENDPOINT=http://localhost:11434/v1`, `OPENAI_API_KEY=ollama`, `MODEL=ministral-3:8b`).
- **Nota de instalación:** `call.py` importa también `python-dotenv`, además de `openai`; el enunciado solo menciona `pip install openai`. Instalé ambos en un entorno `uv`.

## Salida de `python call.py`
```text
Hello!
---
usage        : CompletionUsage(completion_tokens=3, prompt_tokens=18, total_tokens=21, completion_tokens_details=None, prompt_tokens_details=PromptTokensDetails(audio_tokens=None, cache_write_tokens=None, cached_tokens=4, image_tokens=None, text_tokens=None))
finish_reason: stop
```

## Salida de `bash call.sh`
(sin la barra de progreso de curl)
```json
{"id":"chatcmpl-592","object":"chat.completion","created":1795087409,"model":"ministral-3:8b","system_fingerprint":"fp_ollama","choices":[{"index":0,"message":{"role":"assistant","content":"Hey!"},"finish_reason":"stop"}],"usage":{"prompt_tokens":18,"prompt_tokens_details":{"cached_tokens":17},"completion_tokens":3,"total_tokens":21}}
```
Las dos respuestas difieren (`Hello!` / `Hey!`) porque ambas usan `temperature=0.7`. El uso es idéntico: 18 tokens de entrada + 3 de salida = 21.

## Qué cambió al variar la temperatura
Mismo prompt, 5 ejecuciones por temperatura (`temp_experiment.py`; salida completa en `temp_ministral.txt`):

| temperature | respuestas (`ministral-3:8b`) |
|---|---|
| **0.0** | `Hello!` ×5 (idénticas, 3 tokens) |
| **0.7** | `Hello there!`, `Hello!`, `Greetings! How’s your day going?`, `Hello there.`, `Hello!` |
| **1.5** | `Greetings! How’s your day?`, `Hi! 👋`, `Hello! How's your day going?`, `Greetings.`, `Hello!` |

- Con **0.0** el modelo es determinista: siempre la opción más probable.
- Con **0.7** aparece variedad moderada y algunas respuestas se alargan (hasta 11 tokens, aunque el system prompt pide ser escueto).
- Con **1.5** la variedad es mayor (saludos distintos, un emoji, preguntas añadidas) y las respuestas se salen más del «terse». En esta prueba corta no llegó a producir texto incoherente; con respuestas largas el riesgo sería mayor.
- Cada respuesta es una sola muestra, así que son 5 ejemplos por temperatura, no una medición estadística.

## Cambiar de modelo (`MODEL=qwen3:1.7b`, mismo código)
`python call.py` sin tocar el código:
```text
Hello, how can I assist you today?
---
usage        : CompletionUsage(completion_tokens=81, prompt_tokens=27, total_tokens=108, ...)
finish_reason: stop
```
Observaciones (salida en `call_qwen3.txt` y `temp_qwen3.txt`):

- Responde distinto (más «asistente») y **gasta 81 tokens para una respuesta de 9**: Qwen3 «piensa» internamente y esos tokens también se cuentan (y se pagarían en una API de pago).
- Con `max_tokens=300`, una de las 15 llamadas devolvió **respuesta vacía con `finish_reason: length`**: el razonamiento agotó el límite antes de contestar. En `usage` y `finish_reason` se ve el problema; si solo se mira el texto, parece un fallo silencioso.
- Con temperatura 0.0 salió siempre la misma respuesta (5/5), pero en 0.7 y 1.5 casi siempre repite la misma frase, así que la temperatura cambia mucho menos que en Ministral.

## Por qué el mismo código llegó a un modelo distinto
Porque `/v1/chat/completions` es un formato estándar (JSON sobre HTTP) y lo único que identifica al modelo y al proveedor es configuración (`base_url`, `api_key`, `model` en el `.env`); el código no cambia.

## Extra: la Responses API
El repositorio del enunciado solo contiene `call.py`, `call.sh`, `.env.example` y `README.md`; **no existe `responses_openai.py`**, así que no pude ejecutarlo. Probé directamente con curl `POST /v1/responses` contra mi Ollama:

- **Resultado:** HTTP 200 y respuesta válida (`"Hello! 😊 How can I brighten your day today?"`).
- Es decir, mi Ollama 0.40.14 **sí** soporta `/v1/responses`, al contrario de lo que dice el enunciado. Es probable que versiones más antiguas no lo hicieran. No tengo clave de OpenAI, así que no probé la nube.
