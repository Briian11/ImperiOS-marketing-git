"""Reel orgánico R12 «Red flags de una inmobiliaria desorganizada»: sin voz, texto al ritmo de la música.

Uso: python3 build_timeline_r12.py <out.json>
- Todo va en la rejilla de BPM: título, 6 red flags y pregunta de SEC tiempos cada uno y cierre.
- La primera línea de cada flag entra en el tiempo 1 y la segunda (la remata, en cursiva) en el 3.
"""
import json
import sys

BPM = 124
BT = 60 / BPM
SEC = 6            # tiempos por sección (antes 4: iba demasiado rápido)
out = sys.argv[1]

title = 0.0
flags = [round((SEC + SEC * i) * BT, 3) for i in range(6)]
q = round(7 * SEC * BT, 3)
logo = round(8 * SEC * BT, 3)
end = round(logo + 3.2, 2)

B = {"t": title, "flags": flags, "q": q, "logo": logo, "bt": round(BT, 4), "sec": SEC, "end": end}
cues = [(0.0, "sub_drop", -10, 0, 0), (0.0, "hit_metal_02", -12, 0, 0), (2 * BT, "pop_dock_02", -12, 0, 0)]
for i, f in enumerate(flags):
    cues += [(f - .3, "whoosh_short_0" + str(1 + i % 4), -14, (-.4 if i % 2 else .4), 300), (f, ("hit_soft_03", "hit_metal_01")[i % 2], -10, 0, 0),
             (f + 2 * BT, "pop_dock_0" + str(1 + i % 3), -11, 0, 0)]
cues += [(q - .35, "whoosh_long_01", -13, 0, 300), (q, "hit_soft_02", -10, 0, 0), (q + 2 * BT, "click_ui_02", -12, 0, 0),
         (logo - .35, "riser_grid", -17, 0, 300), (logo, "sub_drop", -10, 0, 0), (logo, "logo_sting", -8, 0, 0),
         (logo + 4 * BT * .5, "pop_dock_02", -10, 0, 0), (logo + 2 * BT + .05, "shimmer_glow", -14, 0, 600)]
B["cues"] = [[round(c[0], 3), *c[1:]] for c in cues]
# música: La menor a 124 BPM, groove desde el primer compás
B["music"] = {"bpm": BPM,
              "chords": [["Am", [45, 52, 57, 60, 64]], ["F", [41, 53, 57, 60, 65]], ["C", [48, 55, 60, 64, 67]], ["G", [43, 50, 55, 59, 62]]] * 2,
              "final": [45, 57, 64, 69, 71, 72, 76, 81]}
B.update({"s1": 0.0, "s2": 0.01, "s3": 0.0, "s5": 0.0, "s6": round(end - 1.2, 3)})
tl = {"fps": 60, "duration": end, "beats": B, "note": f"build_timeline_r12.py: {BPM} BPM, sin voz."}
json.dump(tl, open(out, "w"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in B.items() if k not in ("cues", "music")}))
