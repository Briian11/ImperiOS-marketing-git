"""Reel / anuncio R13 «El panel del CEO»: VO + timeline sincronizado con sus palabras (Scribe).

Uso: python3 build_timeline_r13.py <voz.words.json> <voz.mp3|-> <out.json> <out_vo.wav>
- La VO va a atempo TEMPO, tras PRE s de silencio; todos los tiempos se escalan igual. Con «-» como audio solo escribe el timeline.
- Escenas: gancho (h) → dispositivos (d) → embudo por propiedad (e) → comerciales (c) → campañas (m) → lo tedioso (o) →
  «si puedes medirlo, puedes escalarlo» (f) → logo. Una escena que no esté en la voz (corte para anuncios) queda en null.
"""
import json
import subprocess
import sys

TEMPO = 1.07
PRE = 0.3
TAIL = 2.6

w_path, audio, out, vo_out = sys.argv[1:5]
W = json.load(open(w_path))
if audio != "-":
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", audio, "-af",
                    f"aresample=48000,aformat=channel_layouts=mono,atempo={TEMPO}", "-c:a", "pcm_f32le", vo_out], check=True)


def S(i):
    return PRE + W[i][1] / TEMPO


def E(i):
    return PRE + W[i][2] / TEMPO


def find(word, start=0, must=True):
    for i in range(start, len(W)):
        if W[i][0].strip("¿?¡!.,:;…").lower().startswith(word.lower()):
            return i
    if must:
        raise KeyError(word)
    return None


B = {}
inte = find("interesa")
B["h"] = [S(0), S(inte)]
de = find("Desde", inte, False)
B["d"] = [S(de) - .1, S(find("móvil", de)), S(find("tablet", de)), S(find("ordenador", de))] if de is not None else None
cu = find("Cuántas", 0, False)
B["e"] = [S(cu) - .1, S(find("consultas", cu)), S(find("visita", cu)), S(find("oferta", cu)), S(find("No", cu))] if cu is not None else None
qe = find("Qué", 0, False)
B["c"] = ([S(qe) - .1] + [S(find(x, qe)) for x in ("captaciones", "valoraciones", "visitas", "cierres", "mejor")]) if qe is not None else None
ha = find("Haces", 0, False)
B["m"] = ([S(ha) - .1] + [S(find(x, ha)) for x in ("Inversión", "clics", "leads", "directo", "notificación", "reunión")]) if ha is not None else None
pe = find("pesado", 0, False)
B["o"] = ([S(pe - 2) - .1] + [S(find(x, pe)) for x in ("documentación", "facturación", "seguimiento")]) if pe is not None else None
co = [i for i in range(len(W)) if W[i][0] == "Con"][-1]
B["f"] = [S(co) - .1, S(find("números", co)), S(find("medirlo", co)), S(find("escalarlo", co))]
last = len(W) - 1
B["logo"] = S(last) - .1
# notificaciones en el móvil del gancho (cada 0,45 s hasta «interesa»); suenan con un «ding»
B["hn"] = [round(i * .5 - (.4 if i == 0 else 0), 3) for i in range(9) if i * .5 < S(inte) - .3]   # la primera ya está en el fotograma 0
B["dings"] = [x for x in B["hn"] if x >= 0]
B["wt"] = {"h": [round(S(i) - B["h"][0], 3) for i in range(0, inte + 1)],
           "f": [round(S(i) - B["f"][0], 3) for i in range(co, find("escalarlo", co) + 1)]}

# subtítulos de las escenas centrales (frase a frase)
def sub(a, b, hl):
    return {"s": round(S(a) - .08, 3), "e": round(E(b), 3), "w": [[W[i][0], round(S(i), 3), 1 if W[i][0] in hl else 0] for i in range(a, b + 1)]}


SB = []
if de is not None:
    SB.append(sub(de, find("ordenador", de), {"móvil,", "tablet", "ordenador."}))
if cu is not None:
    p1 = find("propiedad", cu); v = find("visita", cu); o = find("oferta", cu); n = find("No", cu); na = find("nada", n)
    SB += [sub(cu, p1, {"propiedad."}), sub(p1 + 1, o, {"visita.", "oferta."}), sub(n, na, {"nada."})]
if qe is not None:
    ci = find("cierres", qe); un = find("uno", ci)
    SB += [sub(qe, ci, {"cierres."}), sub(ci + 1, un, {"mejor"})]
if ha is not None:
    pu = find("publicitarias", ha); di = find("directo", ha); nu = find("nuevo", di); mk = find("marketing", nu)
    SB += [sub(ha, pu, {"publicitarias?"}), sub(pu + 1, di, {"directo."}), sub(di + 1, nu, {"notificación"}), sub(nu + 1, mk, {"mes"})]
if pe is not None:
    si = find("sitio", pe); cm = find("comercial", si)
    SB += [sub(pe - 2, si, {"pesado,"}), sub(si + 1, cm, {"documentación,", "facturación", "seguimiento"})]
B["sub"] = SB

end = E(last) + TAIL
h, d, e, c, m, o, f, lg = (B[x] for x in ("h", "d", "e", "c", "m", "o", "f", "logo"))
cues = [(0.0, "hit_soft_03", -12, 0, 0), (h[1], "pop_dock_02", -12, 0, 0)]
if d:
    cues += [(d[0] - .2, "whoosh_long_02", -12, 0, 250), *[(x, "pop_dock_0" + str(1 + j), -12, (j - 1) * .4, 0) for j, x in enumerate(d[1:])]]
if e:
    cues += [(e[0] - .15, "whoosh_low_wipe", -10, 0, 0), *[(x, "ticks_granular_curve", -18, 0, 0) for x in e[1:4]], (e[4], "hit_soft_02", -10, 0, 0), (e[4] + .05, "shimmer_glow", -14, 0, 600)]
if c:
    cues += [(c[0] - .15, "whoosh_short_02", -13, 0, 300), *[(x, "click_ui_0" + str(1 + j % 3), -14, (j - 1.5) * .3, 0) for j, x in enumerate(c[1:5])],
             *[(c[5] + j * .15, "pop_dock_0" + str(1 + j % 3), -12, 0, 0) for j in range(4)]]
if m:
    cues += [(m[0] - .15, "whoosh_short_03", -13, 0, 300), *[(x, "click_ui_0" + str(1 + j), -14, 0, 0) for j, x in enumerate(m[1:4])],
             (m[4], "ticks_granular_calendar", -18, 0, 0), (m[5] - .1, "pop_dock_03", -9, .3, 0), (m[5] - .05, "shimmer_glow", -15, .3, 600), (m[6] + .3, "glitch_wake", -18, 0, 0)]
if o:
    cues += [(o[0] - .15, "whoosh_long_01", -14, 0, 300), *[(x, "whoosh_short_0" + str(1 + j), -15, (j - 1) * .4, 300) for j, x in enumerate(o[1:])],
             *[(x + .25, "pop_dock_0" + str(1 + j), -13, (j - 1) * .4, 0) for j, x in enumerate(o[1:])]]
cues += [(f[0] - .2, "riser_grid", -16, 0, 300), (f[1], "hit_soft_01", -12, 0, 0), (f[2], "whoosh_short_04", -14, 0, 300), (f[3], "hit_metal_02", -11, 0, 0),
         (lg - .35, "riser_grid", -19, 0, 300), (lg + .05, "sub_drop", -11, 0, 0), (lg + .05, "logo_sting", -9, 0, 0), (lg + .9, "pop_dock_02", -10, 0, 0)]
B["cues"] = [[round(x[0], 3), *x[1:]] for x in cues]
# música: Fa mayor a 100 BPM, elegante; tenso solo en el gancho
B["music"] = {"bpm": 100,
              "chords": [["F", [41, 53, 57, 60, 65]], ["Dm", [38, 50, 57, 62, 65]], ["Bb", [46, 53, 58, 62, 65]], ["C", [48, 55, 60, 64, 67]],
                         ["F", [41, 53, 57, 60, 65]], ["Am", [45, 52, 57, 60, 64]], ["Bb", [46, 53, 58, 62, 65]], ["Csus", [48, 55, 60, 65, 67]]],
              "final": [41, 53, 60, 65, 67, 69, 72, 77]}
first = next(x for x in (d, e, c, m, o) if x)
B.update({"s1": 0.0, "s2": first[0], "s3": 0.0, "s5": 0.0, "s6": f[0]})

for key in ("h", "d", "e", "c", "m", "o", "f"):
    if B[key]:
        B[key] = [round(x, 3) for x in B[key]]
B["logo"] = round(B["logo"], 3)
B["end"] = round(end, 2)
tl = {"fps": 60, "duration": B["end"], "vo_offset": PRE, "beats": B,
      "note": f"build_timeline_r13.py: VO {w_path} a atempo {TEMPO}; offset {PRE} s."}
json.dump(tl, open(out, "w"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in B.items() if k not in ("wt", "cues", "sub", "music")}))
