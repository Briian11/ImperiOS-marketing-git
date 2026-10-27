"""Reel orgánico R9 «Véndela antes de publicarla» (módulo Match): VO + timeline sincronizado con sus palabras (Scribe).

Uso: python3 build_timeline_r9.py <voz.words.json> <voz.mp3> <out.json> <out_vo.wav>
- La VO va a atempo TEMPO (sin cambiar el tono), tras PRE s de silencio; todos los tiempos se escalan igual.
- Escenas: gancho (h) → cartera (c) → propiedad nueva (p) → barrido del match (m) → encajan (e) → reactivar (r) → cierre (q).
- B.sub: subtítulos frase a frase, con la palabra destacada; B.pings: pings del radar para audio_mix.py.
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


por = find("portal")
tie, gen, hoy, nue = find("Tienes"), find("Gente"), find("Hoy"), find("nueva")
con = find("Con", nue)
mat, cru = find("match", con), find("cruza", con)
zon = find("zona", cru)
crit = [zon, find("presupuesto", zon), find("tipo", zon), find("habitaciones", zon)]
y_ = find("Y", crit[3])
enc, aun = find("encajan", y_), find("Aunque", y_)
los, cli = find("Los", aun), find("clic", aun)
ant = find("antes", cli)
cua, com = find("Cuántos", ant), find("Comenta", ant)

B = {"h": [S(0), S(por)],
     "c": [S(tie) - .1, S(gen)],                       # aparece la cartera; «gente que buscaba casa…» la apaga
     "p": [S(hoy) - .05, S(nue)],                      # cae la propiedad nueva; NUEVA
     "m": [S(con) - .05, S(mat), S(cru)],              # arranca el barrido del match
     "crit": [S(i) for i in crit],                     # zona · presupuesto · tipo · habitaciones
     "e": [S(y_) - .05, S(enc), S(aun)],               # se encienden los 3 clientes; «hace X años»
     "r": [S(los) - .15, S(cli), S(ant)],              # fichas + «Reactivar» en un clic; «antes que nadie»
     "q": [S(cua) - .1, S(com)],
     "logo": S(com) - .3}
B["wt"] = {"h": [round(S(i) - B["h"][0], 3) for i in range(0, por + 1)],
           "q": [round(S(i) - B["q"][0], 3) for i in range(cua, find("cartera", cua) + 1)]}

# subtítulos: (primera palabra, última, palabras destacadas); la frase de los criterios no lleva (van los chips)
SUBS = [(tie, gen - 1, {"años."}), (gen, hoy - 1, {"suya."}), (hoy, con - 1, {"nueva."}),
        (con, find("Imperios", con), {"match"}), (find("Imperios", con) + 1, zon - 1, {"cartera:"}),
        (y_, aun - 1, {"encajan."}), (aun, los - 1, {"años"}), (los, cli, {"clic…"}), (cli + 1, cua - 1, {"antes", "que", "nadie."})]
B["sub"] = [{"s": round(S(a) - .08, 3), "e": round(E(b), 3),
             "w": [[W[i][0].replace("Imperios", "ImperiOS"), round(S(i), 3), 1 if W[i][0] in hl else 0] for i in range(a, b + 1)]}
            for a, b, hl in SUBS]
# pings del radar: una vuelta cada 1,2 s mientras barre, más uno por cliente que encaja
B["pings"] = [round(B["m"][1] + i * 1.2, 3) for i in range(int((B["e"][1] - B["m"][1]) / 1.2) + 1)] + [round(B["e"][1] + i * .15, 3) for i in range(3)]

end = E(len(W) - 1) + TAIL
h, c, p, m, e, r, q, lg = B["h"], B["c"], B["p"], B["m"], B["e"], B["r"], B["q"], B["logo"]
# ---- efectos (t, sfx, dB, pan, hpf) ----
cues = [(0.0, "hit_soft_03", -12, 0, 0), (S(find("antes")), "pop_dock_02", -13, 0, 0), (h[1], "click_mech_dial_1", -12, .3, 0), (h[1] + .3, "glitch_wake", -19, .3, 0),
        (c[0] - .25, "whoosh_long_02", -12, 0, 250), (c[0] + .05, "sub_drop", -14, 0, 0), (c[0] + .1, "ticks_granular_curve", -18, 0, 0),
        (c[1] + .2, "suck_reverse", -16, 0, 200),
        (p[0] - .2, "whoosh_short_03", -13, 0, 300), (p[0] + .25, "hit_soft_02", -9, 0, 0), (p[0] + .27, "sub_drop", -13, 0, 0), (p[1], "pop_dock_01", -11, .2, 0),
        (m[0] - .1, "riser_grid", -16, 0, 300), (m[1], "whoosh_low_wipe", -10, 0, 0), (m[1] + .05, "shimmer_glow", -16, 0, 600),
        *[(t, "click_ui_0" + str(1 + j % 3), -14, (j - 1.5) * .3, 0) for j, t in enumerate(B["crit"])],
        *[(e[1] + j * .15, "pop_dock_0" + str(1 + j), -10, (-.4, .4, -.2)[j], 0) for j in range(3)], (e[1] + .05, "shimmer_glow", -13, 0, 600),
        *[(e[2] + .1 + j * .18, "click_ui_0" + str(1 + j), -17, 0, 0) for j in range(3)],
        (r[0] - .1, "whoosh_long_01", -14, 0, 300), *[(r[0] + .2 + j * .12, "pop_dock_0" + str(1 + j), -14, 0, 0) for j in range(3)],
        (r[1], "click_mech_dial_2", -9, 0, 0), (r[1] + .05, "hit_soft_01", -12, 0, 0), *[(r[1] + .2 + j * .12, "click_ui_0" + str(1 + j), -15, 0, 0) for j in range(3)],
        (r[2], "shimmer_glow", -14, 0, 600), (r[2] + .05, "pop_dock_03", -13, 0, 0),
        (q[0] - .2, "whoosh_long_02", -14, 0, 300), (lg - .35, "riser_grid", -19, 0, 300), (lg + .05, "sub_drop", -11, 0, 0),
        (lg + .05, "logo_sting", -9, 0, 0), (q[1] + .3, "pop_dock_02", -9, 0, 0), (q[1] + .35, "shimmer_glow", -15, 0, 600)]
B["cues"] = [[round(x[0], 3), *x[1:]] for x in cues]
# música: Fa# menor a 110 BPM (distinta del R2/R6); tenso hasta que entra la propiedad, groove con el match
B["music"] = {"bpm": 110,
              "chords": [["F#m", [42, 49, 54, 57, 61]], ["D", [38, 50, 54, 57, 62]], ["A", [45, 52, 57, 61, 64]], ["E", [40, 52, 56, 59, 64]],
                         ["F#m", [42, 49, 54, 57, 61]], ["D", [38, 50, 54, 57, 62]], ["Bm", [47, 54, 59, 62, 66]], ["Esus", [40, 52, 57, 59, 64]]],
              "final": [45, 57, 64, 69, 71, 73, 76, 81]}   # La add9 abierto
B.update({"s1": 0.0, "s2": m[1], "s3": c[0], "s5": p[0], "s6": q[0]})

B = {k: (round(v, 3) if isinstance(v, float) else v) for k, v in B.items()}
for key in ("h", "c", "p", "m", "crit", "e", "r", "q"):
    B[key] = [round(x, 3) for x in B[key]]
B["end"] = round(end, 2)
tl = {"fps": 60, "duration": B["end"], "vo_offset": PRE, "beats": B,
      "note": f"build_timeline_r9.py: VO {w_path} a atempo {TEMPO}; offset {PRE} s."}
json.dump(tl, open(out, "w"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in B.items() if k not in ("wt", "cues", "sub", "music", "pings")}))
