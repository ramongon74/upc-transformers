# Informe — Ejercicio 1: Tokenize, locally

Tokenizadores: `gpt2` (BPE a nivel de byte, 2019) vs `bert-base-uncased` (WordPiece, 2018).
Idioma propio: español (párrafo por defecto del script).

## 1. Frase de demo
`"The model never sees the letters in strawberry."` → **9 tokens** con `gpt2`.

## 2. Penalización multilingüe (español vs inglés, gpt2)
- Inglés: 38 tokens
- Español: 63 tokens
- **Penalización = (63 − 38) / 38 = +65,8 %**

## 3. Comparación en entradas de código

| entrada          | gpt2 | bert-base-uncased |
|------------------|-----:|------------------:|
| python function  |   26 |                22 |
| JSON blob        |   36 |                45 |
| regex-heavy line |   41 |                44 |
| whitespace-heavy |   20 |                 5 |

- **python function**: gpt2 gasta más (26 vs 22) porque conserva cada salto de línea y cada espacio de indentación como tokens (`Ċ`, `Ġ`), mientras que BERT los descarta al normalizar el espacio en blanco.
- **JSON blob**: aquí BERT gasta más (45 vs 36) porque separa cada comilla, coma y llave como token independiente, mientras que gpt2 tiene tokens fusionados frecuentes como `{"`, `":`, `",` y `"}`.
- **regex-heavy line**: casi empatan (41 vs 44); ambos fragmentan los símbolos en trozos de 1 carácter porque son secuencias raras en el texto de entrenamiento; BERT además pasa a minúsculas y rompe `A-Za-z` en `a-za-z`, perdiendo información.
- **whitespace-heavy**: es donde más difieren (20 vs 5, 4x) porque BERT elimina tabuladores, saltos de línea y espacios repetidos (no ve la estructura), mientras que gpt2 es byte-level y reversible: cada tabulador y cada espacio extra cuenta como token.

Conclusión: el contraste muestra un compromiso. gpt2 es sin pérdida (se puede reconstruir el texto exacto), por eso es mejor para código donde la indentación importa; BERT es más compacto con espacio en blanco, pero pierde información.
