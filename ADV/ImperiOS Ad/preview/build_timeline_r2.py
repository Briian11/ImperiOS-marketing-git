"""Reel orgánico R2 «3 errores que te hacen perder leads»: VO + timeline sincronizado con sus palabras (Scribe).

Uso: python3 build_timeline_r2.py <voz.words.json> <voz (mp3/wav)> <out.json> <out_vo.wav>
- La VO va a velocidad natural (sin atempo), tras PRE s de silencio.
- Cada escena arranca justo antes de su «Uno / Dos / Tres»; los tiempos de cada bloque son relativos a su escena.
- Escribe también la lista de efectos (beats.cues) que usa audio_mix.py, atada a las mismas palabras.
"""
import json
import subprocess
import sys

PRE = 0.3      # silencio antes de la voz (el titular ya está en pantalla)
TAIL = 2.6     # «Comenta DEMO» + IMPERIOS.APP tras la última palabra

w_path, audio, out, vo_out = sys.argv[1:5]
W = json.load(open(w_path))
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", audio, "-af",
                "aresample=48000,aformat=channel_layouts=mono", "-c:a", "pcm_f32le", vo_out], check=True)


def S(i):
    return PRE + W[i][1]


def E(i):
    return PRE + W[i][2]


def find(word, start=0):
    """Índice de la primera palabra que empieza por `word` (sin puntuación) desde `start`."""
    for i in range(start, len(W)):
        if W[i][0].strip("¿?¡!.,:;").lower().startswith(word.lower()):
            return i
    raise KeyError(word)


uno, dos = find("Uno"), find("Dos")
tres = find("Tres", dos)
cual = find("Cuál")
imp = find("Imperios", cual)
B = {"e1": S(uno) - .15, "e2": S(dos) - .15, "e3": S(tres) - .15, "sv": S(cual) - .2}
B["logo"] = S(imp) - .15
end = E(len(W) - 1) + TAIL
rel = lambda idx, sc: [round(S(i) - B[sc], 3) for i in idx]

per = find("perder")
con, tar, qui = find("contestar"), find("tarde"), find("Quien")
age, pri = find("agencias", qui), find("primera", qui)
res, se_ = find("responde", pri), find("se", pri)
lle = find("lleva", se_)
la2 = find("la", lle)
cnv = find("conversación", lle)
ten = find("tener", dos)
lea, rep = find("leads", ten), find("repartidos", ten)
por, wa, exc = find("portales", rep), find("WhatsApp", rep), find("Excel", rep)
lo_ = find("Lo", exc)
olv = find("olvidarte", tres)
man = find("mañana", olv)
pis = find("piso", man)
wt = {
    "kT": [round(S(per), 3)],
    # contestar, tarde, quien, agencias, primera, responde, se, lleva, la, conversación | «La primera que responde se lleva la conversación.»
    "k1": rel([con, tar, qui, age, pri, res, se_, lle, la2, cnv] + list(range(pri - 1, cnv + 1)), "e1"),
    # tener, leads, repartidos, portales, WhatsApp, Excel | «Lo que no ves, no lo sigues.»
    "k2": rel([ten, lea, rep, por, wa, exc] + list(range(lo_, lo_ + 7)), "e2"),
    # «Olvidar a quien no compró» (olvidarte de quien no compró) | «Mañana puede entrar el piso que busca.»
    "k3": rel(list(range(olv, olv + 5)) + list(range(man, man + 7)), "e3"),
    "k4": rel(list(range(cual, len(W))), "sv"),
}
B["wt"] = wt

# ---- efectos (t, sfx, dB, pan, hpf) ----
e1, e2, e3, sv, lg = B["e1"], B["e2"], B["e3"], B["sv"], B["logo"]
cues = [(0.0, "hit_soft_03", -13, 0, 0), (0.02, "shimmer_glow", -19, 0, 600),
        *[(.5 + i * .35, f"whoosh_short_0{1 + i}", -19, .5, 400) for i in range(3)],
        (S(per), "pop_dock_03", -16, 0, 0)]
cues += [(e1 - .12, "whoosh_long_02", -14, 0, 250), (e1 + .05, "pop_dock_01", -11, -.5, 0),
         (S(qui), "pop_dock_02", -13, 0, 0),
         *[(S(age) - .4 + i * .14, f"click_ui_0{1 + i}", -16, -.3 + i * .3, 0) for i in range(3)],
         (S(res), "pop_dock_03", -11, -.3, 0), (S(res) + .05, "shimmer_glow", -17, -.3, 600),
         (S(lle), "hit_soft_01", -14, .2, 0)]
cues += [(e2 - .15, "whoosh_low_wipe", -11, 0, 0), (e2 + .05, "pop_dock_01", -11, -.5, 0),
         (S(por), "pop_dock_02", -12, -.5, 0), (S(wa), "pop_dock_03", -12, 0, 0), (S(exc), "pop_dock_01", -12, .5, 0),
         *[(S([por, wa, exc][i % 3]) + .2 + (i // 3) * .1, f"click_ui_0{1 + i % 3}", -20, (i % 3 - 1) * .5, 0) for i in range(6)],
         (S(lo_ + 2), "suck_reverse", -14, 0, 200), (S(lo_ + 2) + .1, "whoosh_long_01", -18, 0, 300)]
cues += [(e3 - .15, "whoosh_long_01", -14, 0, 300), (e3 + .05, "pop_dock_01", -11, -.5, 0),
         (S(olv + 2), "pop_dock_02", -14, 0, 0), (S(man + 1), "whoosh_short_02", -13, .6, 300), (S(man + 1) + .4, "pop_dock_02", -12, .4, 0),
         (S(pis) - .2, "ticks_granular_curve", -19, 0, 0), (S(pis), "hit_soft_02", -10, 0, 0), (S(pis) + .05, "click_mech_dial_2", -13, .3, 0),
         (S(pis) + .1, "shimmer_glow", -15, 0, 600)]
dem = find("demo", imp)
cues += [(sv - .05, "whoosh_short_04", -12, 0, 300), (S(cual), "pop_dock_01", -9, 0, 0), (S(cual) + .05, "hit_soft_03", -12, 0, 0),
         (S(cual + 7), "click_ui_02", -14, .3, 0),
         (lg - .35, "riser_grid", -19, 0, 300), (lg - .1, "whoosh_short_02", -14, 0, 300), (lg + .05, "sub_drop", -11, 0, 0), (lg + .05, "logo_sting", -9, 0, 0),
         (S(dem - 1) - .05, "whoosh_short_04", -14, 0, 300), (S(dem - 1) + .3, "pop_dock_02", -9, 0, 0), (S(dem - 1) + .35, "shimmer_glow", -15, 0, 600)]
B["cues"] = [[round(c[0], 3), *c[1:]] for c in cues]
# música: arranca con el titular, groove desde el error 1, sin tramo oscuro, acorde final bajo el logo
B.update({"s1": 0.0, "s2": e1, "s3": lg, "s5": lg, "s6": lg - .6})

B = {k: (round(v, 3) if isinstance(v, float) else v) for k, v in B.items()}
B["end"] = round(end, 2)
tl = {"fps": 60, "duration": B["end"], "vo_offset": PRE, "beats": B,
      "note": f"build_timeline_r2.py: VO {w_path} a velocidad natural; offset {PRE} s."}
json.dump(tl, open(out, "w"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in B.items() if k not in ("wt", "cues")}))
