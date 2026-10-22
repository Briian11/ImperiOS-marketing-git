"""Reel orgánico R6 «Antes / después»: VO + timeline sincronizado con sus palabras (Scribe).

Uso: python3 build_timeline_r6.py <voz.words.json> <voz.mp3> <out.json> <out_vo.wav>
- La VO va a atempo TEMPO (sin cambiar el tono), tras PRE s de silencio; todos los tiempos se escalan igual.
- B.a / B.d: inicio de cada bloque del ANTES / DESPUÉS (titular + su visual); B.wt: tiempos finos relativos a cada bloque.
- Escribe también la lista de efectos (beats.cues) que usa audio_mix.py, atada a las mismas palabras.
"""
import json
import subprocess
import sys

TEMPO = 1.07
PRE = 0.3      # silencio antes de la voz (la etiqueta ANTES ya está en pantalla)
TAIL = 2.6     # «Comenta DEMO» + IMPERIOS.APP tras la última palabra

w_path, audio, out, vo_out = sys.argv[1:5]
W = json.load(open(w_path))
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", audio, "-af",
                f"aresample=48000,aformat=channel_layouts=mono,atempo={TEMPO}", "-c:a", "pcm_f32le", vo_out], check=True)


def S(i):
    return PRE + W[i][1] / TEMPO


def E(i):
    return PRE + W[i][2] / TEMPO


def find(word, start=0):
    """Índice de la primera palabra que empieza por `word` (sin puntuación) desde `start`."""
    for i in range(start, len(W)):
        if W[i][0].strip("¿?¡!.,:;…").lower().startswith(word.lower()):
            return i
    raise KeyError(word)


ant, tar, lue = find("Antes"), find("Tardas"), find("Luego")
inf = find("información", lue)
pie = find("pierde", inf)
vis = find("visita", pie)
rec = find("recordatorio", vis)
no_ = find("no", rec)
des = find("Después", no_)
con = find("con", des)
en_ = find("En", find("centralizado", con))
res = find("responde", en_)
enf = find("enfría", res)
el3 = enf - 4                       # «El cliente no se enfría»
cnv = find("conversación", enf)
vis2 = find("visita", cnv)
y5 = find("Y", vis2)
ubi, dia, hor = find("ubicación", y5), find("día", y5), find("hora", y5)
tu = find("Tu", hor)
com = find("Comenta", tu)

B = {"a": [S(ant), S(tar) - .1, S(lue) - .1, S(vis - 1) - .1, S(rec - 1) - .1],
     "d0": S(des) - .1,
     "d": [S(con) - .1, S(en_) - .1, S(el3) - .1, S(cnv - 1) - .1, S(y5) - .1],
     "c0": S(tu) - .15}
B["logo"] = S(com) - .35
end = E(len(W) - 1) + TAIL
a, d, c0 = B["a"], B["d"], B["c0"]
B["wt"] = {
    "a3i": round(S(pie) - a[2], 3),                 # los datos del cliente se desvanecen al decir «se pierde»
    "a5n": round(S(no_) - a[4], 3),                 # sello «NO SE PRESENTÓ»
    "d2r": round(S(res) - d[1], 3),                 # la IA responde
    "d4v": round(S(vis2) - d[3], 3),                # la visita aparece en la ficha
    "d5c": [round(S(i) - d[4], 3) for i in (ubi, dia, hor)],
    # ¿Tu inmobiliaria sigue en el antes? | Comenta demo | y te enseño el después.
    "c": [round(S(i) - c0, 3) for i in range(tu, len(W))],
}

# ---- efectos (t, sfx, dB, pan, hpf) ----
lg = B["logo"]
cues = [(a[0] + .3, "pop_dock_01", -12, -.3, 0), (a[0] + .35, "click_ui_01", -16, -.3, 0)]
cues += [(a[1] + .25 + i * .32, ["pop_dock_02", "click_ui_02", "pop_dock_03", "click_ui_03", "pop_dock_01", "click_ui_01", "pop_dock_02", "click_ui_02"][i], -15, (i % 3 - 1) * .5, 0) for i in range(8)]
cues += [(a[2] - .1, "whoosh_short_02", -14, .5, 300), (a[2] + .9, "whoosh_long_01", -16, .6, 300),
         (S(pie), "suck_reverse", -14, 0, 200), (S(pie) + .1, "glitch_wake", -18, 0, 0),
         (a[3] + .1, "pop_dock_03", -12, 0, 0), (a[3] + .15, "hit_soft_01", -16, 0, 0),
         (a[4] + .1, "pop_dock_02", -13, .4, 0), (a[4] + .9, "click_mech_dial_1", -12, .4, 0),
         (S(no_), "hit_metal_02", -12, 0, 0), (S(no_) + .02, "hit_soft_03", -11, 0, 0)]
cues += [(B["d0"] - 1.0, "riser_grid", -15, 0, 300), (B["d0"] - .15, "whoosh_low_wipe", -9, 0, 0),
         (B["d0"] + .05, "hit_soft_03", -9, 0, 0), (B["d0"] + .1, "shimmer_glow", -14, 0, 600),
         *[(d[0] + .4 + i * .3, f"whoosh_short_0{1 + i}", -16, (-.5 if i % 2 == 0 else .5), 400) for i in range(4)],
         *[(d[0] + .75 + i * .3, "click_ui_0" + str(1 + i % 3), -18, 0, 0) for i in range(4)],
         (S(find("centralizado", con)), "hit_soft_02", -12, 0, 0),
         (d[1], "pop_dock_01", -12, 0, 0), (d[1] + .5, "pop_dock_02", -13, -.4, 0), (d[1] + .5, "ticks_granular_curve", -20, 0, 0),
         (S(res), "pop_dock_03", -10, .4, 0), (S(res) + .05, "shimmer_glow", -15, .3, 600), (S(res) + .5, "click_mech_dial_2", -14, .4, 0),
         (d[2], "whoosh_short_03", -15, 0, 300), (d[2] + .3, "ticks_granular_calendar", -19, 0, 0), (d[2] + 1.0, "hit_soft_01", -14, 0, 0),
         (d[3] - .2, "whoosh_long_02", -14, 0, 250), (d[3] + .1, "pop_dock_01", -12, 0, 0), (S(vis2), "pop_dock_02", -12, .2, 0),
         (d[4] + .1, "pop_dock_03", -12, 0, 0),
         *[(S(i), f"click_ui_0{1 + j}", -14, (j - 1) * .4, 0) for j, i in enumerate((ubi, dia, hor))],
         (S(hor) + .5, "shimmer_glow", -14, 0, 600), (S(hor) + .5, "hit_soft_02", -12, 0, 0)]
cues += [(c0 - .2, "whoosh_long_01", -14, 0, 300), (lg - .35, "riser_grid", -19, 0, 300), (lg + .05, "sub_drop", -11, 0, 0),
         (lg + .05, "logo_sting", -9, 0, 0), (S(com) - .05, "whoosh_short_04", -14, 0, 300), (S(com) + .3, "pop_dock_02", -9, 0, 0),
         (S(com) + .35, "shimmer_glow", -15, 0, 600)]
B["cues"] = [[round(x[0], 3), *x[1:]] for x in cues]
# música: ANTES con el filtro oscuro y hats (tensión), groove desde el DESPUÉS, acorde final bajo el logo
B.update({"s1": 0.0, "s2": B["d0"], "s3": 0.3, "s5": B["d0"], "s6": c0})

B = {k: (round(v, 3) if isinstance(v, float) else ([round(x, 3) for x in v] if k in ("a", "d") else v)) for k, v in B.items()}
B["end"] = round(end, 2)
tl = {"fps": 60, "duration": B["end"], "vo_offset": PRE, "beats": B,
      "note": f"build_timeline_r6.py: VO {w_path} a atempo {TEMPO}; offset {PRE} s."}
json.dump(tl, open(out, "w"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in B.items() if k not in ("wt", "cues")}))
