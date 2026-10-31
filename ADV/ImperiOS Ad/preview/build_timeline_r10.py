"""Reel orgánico R10 «¿Qué campaña te trae clientes?» (módulo de marketing): VO + timeline sincronizado con sus palabras (Scribe).

Uso: python3 build_timeline_r10.py <voz.words.json> <voz.mp3> <out.json> <out_vo.wav>
- La VO va a atempo TEMPO (sin cambiar el tono), tras PRE s de silencio; todos los tiempos se escalan igual.
- Escenas: gancho (h) → embudos (f) → panel de clientes con origen y rendimiento (p) → ranking y presupuesto (s) →
  lanzar campaña desde el CRM (l) → cierre (q). B.sub: subtítulos; B.coins: monedas para audio_mix.py.
"""
import json
import subprocess
import sys

TEMPO = 1.07
PRE = 0.3
TAIL = 2.4
COIN_GAP = .3      # una moneda cada 0,3 s por embudo (el motor usa el mismo valor)

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


pre = find("presupuesto")
tie, tod, per = find("Tienes"), find("Todos"), find("Pero")
cl2 = find("clientes", per)
con = find("Con", cl2)
ent, ori = find("entra", con), find("origen", con)
yv = find("Y", ori)
ren, pan = find("rendimiento", yv), find("panel", yv)
asi = find("Así", pan)
fun, don, pr2 = find("funciona", asi), find("dónde", asi), find("presupuesto", asi)
yl = find("Y", pr2)
lan, crm = find("lanzas", yl), find("CRM", yl)
sab = find("Sabes", crm)
com = find("Comenta", sab)

B = {"h": [S(0), S(find("clientes")), S(find("cuál")), S(pre)],
     "f": [S(tie) - .1, S(tod), S(per), S(cl2)],                 # embudos: entran, «todos gastan», «pero no todos…», «clientes»
     "p": [S(con) - .1, S(ent), S(ori), S(ren), S(pan)],          # panel: clientes con origen → rendimiento
     "s": [S(asi) - .1, S(fun), S(don), S(pr2)],                  # ranking y presupuesto
     "l": [S(yl) - .1, S(lan), S(crm)],                           # lanzar campaña
     "q": [S(sab) - .1, S(com)],
     "logo": S(com) - .3}
B["wt"] = {"h": [round(S(i) - B["h"][0], 3) for i in range(0, pre + 1)],
           "q": [round(S(i) - B["q"][0], 3) for i in range(sab, find("mejor", sab) + 1)]}
SUBS = [(tie, tod - 1, {"vez."}), (tod, per - 1, {"gastan."}), (per, cl2, {"clientes."}), (con, ori, {"origen."}),
        (yv, pan, {"panel."}), (asi, fun, {"funciona…"}), (fun + 1, pr2, {"presupuesto."}), (yl, crm, {"CRM."})]
B["sub"] = [{"s": round(S(a) - .08, 3), "e": round(E(b), 3),
             "w": [[W[i][0].replace("Imperios", "ImperiOS"), round(S(i), 3), 1 if W[i][0] in hl else 0] for i in range(a, b + 1)]}
            for a, b, hl in SUBS]
# monedas: caen en la boca de cada embudo 0,5 s después de aparecer; una de cada dos suena
f0, p0 = B["f"][0], B["p"][0]
coins = []
for f in range(3):
    j = 0
    while True:
        land = f0 + .3 + j * COIN_GAP + f * .1 + .5
        if land > p0 + .2:
            break
        if j % 2 == f % 2:
            coins.append(round(land, 3))
        j += 1
B["coins"] = sorted(coins)

end = E(len(W) - 1) + TAIL
h, f, p, s_, l, q, lg = B["h"], B["f"], B["p"], B["s"], B["l"], B["q"], B["logo"]
cues = [(0.0, "hit_soft_03", -12, 0, 0), (h[1], "pop_dock_02", -13, -.2, 0), (h[3], "glitch_wake", -18, .2, 0), (h[3] + .05, "hit_soft_01", -13, 0, 0),
        (f[0] - .2, "whoosh_long_02", -12, 0, 250), (f[0] + .15, "pop_dock_01", -13, -.5, 0), (f[0] + .25, "pop_dock_02", -13, 0, 0), (f[0] + .35, "pop_dock_03", -13, .5, 0),
        (f[1], "ticks_granular_curve", -18, 0, 0), (f[2], "suck_reverse", -15, 0, 200),
        *[(f[3] + j * .15, "pop_dock_0" + str(1 + j % 3), -14, (j - 1) * .5, 0) for j in range(3)], (f[3] + .2, "hit_metal_02", -16, 0, 0),
        (p[0] - .15, "whoosh_low_wipe", -10, 0, 0), (p[0] + .3, "hit_soft_02", -11, 0, 0),
        *[(p[1] + j * .22, "click_ui_0" + str(1 + j % 3), -15, 0, 0) for j in range(4)], (p[2], "shimmer_glow", -16, 0, 600),
        (p[3] - .1, "whoosh_short_02", -14, 0, 300), (p[3] + .2, "ticks_granular_calendar", -19, 0, 0),
        (s_[1], "whoosh_short_03", -14, 0, 300), (s_[1] + .3, "pop_dock_03", -10, 0, 0), (s_[1] + .35, "shimmer_glow", -15, 0, 600),
        (s_[2] + .1, "riser_grid", -18, 0, 300), *[(s_[3] + j * .12, "pop_dock_0" + str(1 + j), -14, (.4 - .3 * j), 0) for j in range(3)],
        (l[0] - .15, "whoosh_long_01", -13, 0, 300), (l[0] + .3, "pop_dock_01", -13, 0, 0),
        (l[1], "click_mech_dial_2", -9, 0, 0), (l[1] + .05, "hit_soft_01", -12, 0, 0), (l[2], "shimmer_glow", -14, 0, 600), (l[2] + .05, "pop_dock_03", -12, 0, 0),
        (q[0] - .2, "whoosh_long_02", -14, 0, 300), (lg - .35, "riser_grid", -19, 0, 300), (lg + .05, "sub_drop", -11, 0, 0),
        (lg + .05, "logo_sting", -9, 0, 0), (q[1] + .3, "pop_dock_02", -9, 0, 0), (q[1] + .35, "shimmer_glow", -15, 0, 600)]
B["cues"] = [[round(x[0], 3), *x[1:]] for x in cues]
# música: Si bemol mayor a 104 BPM (distinta del R2/R6 y del R9)
B["music"] = {"bpm": 104,
              "chords": [["Bb", [46, 53, 58, 62, 65]], ["Gm", [43, 50, 55, 58, 62]], ["Eb", [39, 51, 55, 58, 63]], ["F", [41, 53, 57, 60, 65]],
                         ["Bb", [46, 53, 58, 62, 65]], ["Gm", [43, 50, 55, 58, 62]], ["Cm", [48, 55, 60, 63, 67]], ["Fsus", [41, 53, 58, 60, 65]]],
              "final": [34, 46, 53, 58, 60, 62, 65, 72]}   # Si bemol add9 abierto
B.update({"s1": 0.0, "s2": p[0], "s3": f[2], "s5": p[0], "s6": q[0]})

for key in ("h", "f", "p", "s", "l", "q"):
    B[key] = [round(x, 3) for x in B[key]]
B["logo"] = round(B["logo"], 3)
B["end"] = round(end, 2)
tl = {"fps": 60, "duration": B["end"], "vo_offset": PRE, "beats": B,
      "note": f"build_timeline_r10.py: VO {w_path} a atempo {TEMPO}; offset {PRE} s."}
json.dump(tl, open(out, "w"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in B.items() if k not in ("wt", "cues", "sub", "music", "coins")}))
