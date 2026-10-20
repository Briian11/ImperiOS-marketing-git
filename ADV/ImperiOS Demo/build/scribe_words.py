"""Convierte el words.json de Scribe (descargado de words_download_url) a [[palabra, inicio, fin], …].
Uso: python3 build/scribe_words.py <scribe.json> vo/<clip>.words.json"""
import json
import sys

d = json.load(open(sys.argv[1]))
ws = d["words"] if isinstance(d, dict) else d
out = [[w["text"], round(w["start"], 3), round(w["end"], 3)] for w in ws if w.get("type", "word") == "word"]
json.dump(out, open(sys.argv[2], "w"), ensure_ascii=False)
print(len(out), "palabras ·", " ".join(w[0] for w in out))
