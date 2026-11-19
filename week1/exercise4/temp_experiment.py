"""Mismo prompt que call.py, variando temperatura (y modelo). Uso: python temp_experiment.py [modelo]"""
import os, sys
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
c = OpenAI(base_url=os.environ["OPENAI_ENDPOINT"], api_key=os.environ["OPENAI_API_KEY"])
model = sys.argv[1] if len(sys.argv) > 1 else os.environ["MODEL"]
print("modelo:", model)
for t in (0.0, 0.7, 1.5):
    print(f"\n--- temperature={t}")
    for i in range(5):
        r = c.chat.completions.create(model=model, temperature=t, max_tokens=300, messages=[
            {"role": "system", "content": "You are a terse assistant."},
            {"role": "user", "content": "Say hello in one sentence."}])
        print(f"  {i+1}. {r.choices[0].message.content!r}  (tokens={r.usage.completion_tokens}, finish={r.choices[0].finish_reason})")
