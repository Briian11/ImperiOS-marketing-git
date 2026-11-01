"""Reel orgánico R11 «Falso interés» (calificación con IA): VO + timeline sincronizado con sus palabras (Scribe).

Uso: python3 build_timeline_r11.py <voz.words.json> <voz.mp3> <out.json> <out_vo.wav>
- La VO va a atempo TEMPO (sin cambiar el tono), tras PRE s de silencio; todos los tiempos se escalan igual.
- Escenas: gancho (h) → avalancha de mensajes (a) → bandeja sin filtrar (b) → filtro de preguntas de la IA (f) →
  curiosos / templados / interesados (c) → prioridad de hoy (p) → cierre (q). B.sub: subtítulos; B.dings: avisos de mensaje.
"""
import json
import subprocess
import sys

TEMPO = 1.07
PRE = 0.3
TAIL = 2.4

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


pre = find("preguntar")
te = find("Te", pre)
n20, n30, n50 = find("veinte"), find("treinta"), find("cincuenta")
ym = find("muchas", n50) - 1
com1 = find("comprar", ym)
tu = find("Tu", com1)
igu = find("igual", tu)
mie = find("mientras", igu)
com2, esp = find("comprar", mie), find("espera", mie)
con = find("Con", esp)
ia, cto, pq, cal = find("inteligencia", con), find("contacto", con), find("preguntas", con), find("calificarlo", con)
asi = find("Así", cal)
cur, inte = find("curiosos", asi), find("interesados", asi)
yt = find("Y", inte)
cme, lla, pri = find("comerciales", yt), find("llamar", yt), find("primero", yt)
cua = find("Cuánto", pri)
fal = find("falso", cua)
cm = find("Comenta", cua)

B = {"h": [S(0), S(pre)],
     "a": [S(te) - .1, S(n20), S(n30), S(n50), S(ym), S(com1)],
     "b": [S(tu) - .1, S(igu), S(mie), S(com2), S(esp)],
     "f": [S(con) - .1, S(ia), S(cto), S(pq), S(cal)],
     "c": [S(asi) - .1, S(cur), S(inte)],
     "p": [S(yt) - .1, S(cme), S(lla), S(pri)],
     "q": [S(cua) - .1, S(cm)],
     "logo": S(cm) - .3}
B["wt"] = {"h": [round(S(i) - B["h"][0], 3) for i in range(0, pre + 1)],
           "q": [round(S(i) - B["q"][0], 3) for i in range(cua, fal + 2)]}
SUBS = [(te, ym - 1, {"portales."}), (ym, com1, {"comprar."}), (tu, igu, {"igual."}), (mie, esp, {"espera."}),
        (con, cto, {"contacto"}), (cto + 1, cal, {"calificarlo."}), (asi, inte + 2, {"curiosos", "interesados"}), (yt, pri, {"primero."})]
B["sub"] = [{"s": round(S(a) - .08, 3), "e": round(E(b), 3),
             "w": [[W[i][0].replace("Imperios", "ImperiOS"), round(S(i), 3), 1 if W[i][0] in hl else 0] for i in range(a, b + 1)]}
            for a, b, hl in SUBS]
h, a, b, f, c, p, q, lg = B["h"], B["a"], B["b"], B["f"], B["c"], B["p"], B["q"], B["logo"]
# avisos de mensaje: 3 en el gancho, y en la avalancha cada vez más seguidos (el motor usa los mismos tiempos)
dings = [h[0] + .5, h[0] + 1.6, h[0] + 2.7]
t = a[0] + .2
while t < a[4]:
    gap = .55 if t < a[2] else (.32 if t < a[3] else .18)
    dings.append(round(t, 3))
    t += gap
B["dings"] = [round(x, 3) for x in dings]

end = E(len(W) - 1) + TAIL
cues = [(0.0, "hit_soft_03", -12, 0, 0), (h[1], "glitch_wake", -18, 0, 0),
        (a[0] - .2, "whoosh_long_02", -12, 0, 250), *[(x, "hit_soft_0" + str(1 + j), -12, 0, 0) for j, x in enumerate(a[1:4])],
        (a[4], "suck_reverse", -15, 0, 200),
        (b[0] - .15, "whoosh_short_03", -13, 0, 300), (b[1], "ticks_granular_curve", -18, 0, 0), (b[3], "pop_dock_02", -12, .3, 0),
        (b[4], "click_mech_dial_1", -13, .3, 0), (b[4] + .05, "glitch_wake", -19, 0, 0),
        (f[0] - .15, "whoosh_low_wipe", -9, 0, 0), (f[0] + .2, "hit_soft_02", -11, 0, 0),
        *[(f[1] + j * .25, "click_ui_0" + str(1 + j % 3), -14, (j - 1.5) * .3, 0) for j in range(4)], (f[1] + .1, "shimmer_glow", -16, 0, 600),
        (f[2], "ticks_granular_calendar", -17, 0, 0), (f[4], "pop_dock_03", -10, 0, 0), (f[4] + .05, "shimmer_glow", -14, 0, 600),
        (c[0] - .1, "whoosh_long_01", -14, 0, 300), (c[1], "pop_dock_01", -13, -.4, 0), (c[2], "pop_dock_03", -10, .4, 0), (c[2] + .05, "shimmer_glow", -14, .4, 600),
        (p[0] - .1, "whoosh_short_02", -13, 0, 300), *[(p[0] + .3 + j * .15, "pop_dock_0" + str(1 + j), -13, 0, 0) for j in range(3)],
        (p[3], "click_mech_dial_2", -9, 0, 0), (p[3] + .05, "hit_soft_01", -12, 0, 0),
        (q[0] - .2, "whoosh_long_02", -14, 0, 300), (lg - .35, "riser_grid", -19, 0, 300), (lg + .05, "sub_drop", -11, 0, 0),
        (lg + .05, "logo_sting", -9, 0, 0), (q[1] + .3, "pop_dock_02", -9, 0, 0), (q[1] + .35, "shimmer_glow", -15, 0, 600)]
B["cues"] = [[round(x[0], 3), *x[1:]] for x in cues]
# música: Do menor a 116 BPM (tensa hasta el filtro); groove cuando entra ImperiOS
B["music"] = {"bpm": 116,
              "chords": [["Cm", [36, 48, 55, 60, 63]], ["Ab", [44, 51, 56, 60, 63]], ["Eb", [39, 51, 55, 58, 63]], ["Bb", [46, 53, 58, 62, 65]],
                         ["Cm", [36, 48, 55, 60, 63]], ["Ab", [44, 51, 56, 60, 63]], ["Fm", [41, 53, 56, 60, 65]], ["G", [43, 50, 55, 59, 62]]],
              "final": [39, 51, 58, 63, 65, 67, 70, 75]}   # Mi bemol add9 abierto
B.update({"s1": 0.0, "s2": f[0], "s3": a[0], "s5": f[0], "s6": q[0]})

for key in ("h", "a", "b", "f", "c", "p", "q"):
    B[key] = [round(x, 3) for x in B[key]]
B["logo"] = round(B["logo"], 3)
B["end"] = round(end, 2)
tl = {"fps": 60, "duration": B["end"], "vo_offset": PRE, "beats": B,
      "note": f"build_timeline_r11.py: VO {w_path} a atempo {TEMPO}; offset {PRE} s."}
json.dump(tl, open(out, "w"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in B.items() if k not in ("wt", "cues", "sub", "music", "dings")}))
