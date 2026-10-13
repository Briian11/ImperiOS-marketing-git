"""Construye el timeline de campaña sincronizado con la VO a partir de los tiempos de palabra (ElevenLabs Scribe).

Uso: python3 build_timeline_vo.py <words.json> <offset_s> <out.json>
Cada bloque de texto en pantalla toma el inicio real de la palabra hablada; las escenas arrancan
justo antes de la frase que las narra (re-temporizar la imagen a la voz, no al revés).
"""
import json
import sys

words_path, OFF, out = sys.argv[1], float(sys.argv[2]), sys.argv[3]
W = [(w, s + OFF, e + OFF) for w, s, e in json.load(open(words_path))]


def at(i):
    return round(W[i][1], 3)


B = {}
B["hook"] = round(W[9][1] - 0.1, 3)        # el pixel nace justo antes de «Con Imperios»
B["s1"] = round(B["hook"] + 0.6, 3)        # chips de origen durante «Con Imperios»
B["s2"] = round(W[11][1] + 0.08, 3)        # «todos entran en un solo panel»
B["s3"] = round(W[22][1] - 0.13, 3)        # «La inteligencia artificial…»
B["s4"] = round(W[33][1] - 0.13, 3)        # «Y cuando hay match…»
B["s5"] = round(W[44][1] - 0.13, 3)        # «Visitas…»
B["s6"] = round(W[53][1] - 0.13, 3)        # «Imperios.»
B["logo"] = round(W[59][2] + 0.03, 3)      # tras «fin.»
B["cta"] = round(W[62][1] + 0.33, 3)       # «demo» → botón
B["end"] = round(W[62][2] + 2.4, 2)


def rel(idx, scene):
    return [round(at(i) - B[scene], 3) for i in idx]


wt = {
    "ktH": [round(at(i), 3) for i in range(0, 9)],
    "kt2": rel([11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21], "s2"),
    "kt3": [round(at(26) - B["s3"], 3), round((at(26) + at(27)) / 2 - B["s3"], 3), round(at(27) - B["s3"], 3),
            round((at(27) + at(29)) / 2 - B["s3"], 3), round(at(29) - B["s3"], 3)],
    "kt3b": rel([30, 31, 32], "s3"),
    "kt4": rel([37, 38, 39, 40, 41, 42, 43], "s4"),
    "kt5": rel([44, 45, 46, 47, 49, 50, 51, 52], "s5"),   # en pantalla: «…agentes, desde la misma agenda.»
    "kt6": rel([54, 55, 56, 57, 58, 59], "s6"),
}
B["wt"] = wt
B["hideKt1"] = True
tl = {"fps": 60, "duration": B["end"], "vo_offset": OFF, "beats": B,
      "note": "Generado por build_timeline_vo.py desde los tiempos de palabra de la VO (toma 1)."}
json.dump(tl, open(out, "w"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in B.items() if k != "wt"}))
