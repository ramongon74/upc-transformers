"""Ejercicio 3: lanza pruebas contra un modelo de Ollama (conversación nueva por prueba)
y guarda las respuestas en results.json. Uso: python3 run_tests.py [modelo]"""
import json, sys, time, urllib.request

MODEL = sys.argv[1] if len(sys.argv) > 1 else "ministral-3:8b"
TESTS = {
 "1. tarea sin ejemplos": "Resume en dos frases por qué el cielo es azul, para un niño de 10 años.",
 "2. regla inventada (few-shot)": "Regla secreta. Ejemplos:\nluna -> anul\nsol -> los\nmar -> ram\nAplica la misma regla a: gato ->",
 "3. formato estricto (JSON)": 'Devuelve SOLO un JSON válido, sin texto adicional ni markdown, con los campos "pais", "capital" y "habitantes_aprox" para Japón.',
 "4. otro idioma": "Explica en català què és un token en un model de llenguatge, en tres línies.",
 "5. código": "Escribe en Python una función que diga si una cadena es un palíndromo ignorando espacios y mayúsculas, con dos tests.",
 "6a. confiadamente equivocado (letras)": "¿Cuántas letras 'r' hay en la palabra 'strawberry'?",
 "6b. confiadamente equivocado (inexistente)": "Resume el argumento del libro 'La biblioteca de cristal de Anselmo Ferrán' (2011) y cita su primer párrafo.",
 "6c. confiadamente equivocado (aritmética)": "Calcula 48217 * 3906 y da solo el resultado.",
}
def chat(p):
    req = urllib.request.Request("http://localhost:11434/api/chat", json.dumps({
        "model": MODEL, "stream": False,
        "messages": [{"role": "user", "content": p}]}).encode(),
        {"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=900))["message"]["content"]
res = {}
for k, p in TESTS.items():
    t = time.time(); res[k] = {"prompt": p, "respuesta": chat(p), "segundos": round(time.time()-t, 1)}
    print("="*60, k, "\n", res[k]["respuesta"], flush=True)
json.dump({"modelo": MODEL, "resultados": res}, open("results.json", "w"), ensure_ascii=False, indent=2)
