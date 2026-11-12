"""Reel R6 «Antes / después» con planos de vídeo de Higgsfield (versión anuncio): VO + timeline sincronizado (Scribe).

Uso: python3 build_timeline_r6h.py <voz.words.json> <voz.wav> <out.json> <out_vo.wav>
- La VO va a atempo TEMPO (sin cambiar el tono), tras PRE s de silencio; todos los tiempos se escalan igual.
- B.v: tramos de vídeo de fondo [id, inicio, fin, zoom0, zoom1] (fotogramas en src/r6h/<id>/, 24 fps, ver prep_r6h_clips.sh).
- B.a: titulares del ANTES (sobre los planos); B.x: «del caos al orden» (avisos que estallan y se recogen en el portátil);
  B.lap2: portátil con ImperiOS y zoom a su panel; B.d: escenas del DESPUÉS (interfaz recreada);
  B.f: titulares de los planos 4 y 5; B.c0 / B.logo: cierre con CTA.
- Escribe también la lista de efectos (beats.cues) que usa audio_mix.py, atada a las mismas palabras.
"""
import json
import subprocess
import sys
from pathlib import Path

TEMPO = 1.07
PRE = 0.15     # el gancho está en pantalla desde el fotograma 0
TAIL = 2.6     # CTA + IMPERIOS.APP tras la última palabra

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


pie0, y0, gan = find("pierde"), find("y"), find("gana")      # gancho «Así se pierde un cliente… y así se gana.»
ant = find("Antes")
men, lla, par = find("mensajes", ant), find("llamadas", ant), find("parar", ant)
la, vis, pap = find("La", ant), find("visita", ant), find("papel", ant)
en_p = pap - 1
y1 = find("y", pap)
pre = find("presenta", y1)
des = find("Después", pre)
con = find("con", des)
en_ = find("En", find("centralizado", con))
res = find("responde", en_)
enf = find("enfría", res)
el3 = enf - 4                       # «El cliente no se enfría»
cnv = find("conversación", enf)
vis2 = find("visita", cnv)
y5 = find("Y", vis2)
ubi, dia, hor = find("ubicación", y5), find("día", y5), find("hora", y5)
mc = find("Menos", hor)
y6 = find("Y", mc)
vie = find("viene", y6)
tu = find("Tu", vie)
com = find("Pide", tu)            # cierre: «Pide tu demo gratis y pasa al después.»

c0 = S(tu) - .15
B = {"h": [S(pie0), S(gan)], "a": [S(ant) - .05, S(la) - .06, S(y1) - .06]}
B["x"] = [S(pre) + .45, E(pre) + .3]                       # caos: estallan los avisos / se recogen
B["lap2"] = [B["x"][1], S(des) - .05, S(con) - .15]        # el portátil sube con los avisos dentro, zoom al panel
B["d"] = [S(con) - .1, S(en_) - .1, S(el3) - .1, S(cnv - 1) - .1, S(y5) - .1]
B["f"] = [S(hor) + 1.0, S(y6) - .06]                       # plano 4 tras «Visita confirmada»; plano 5 en «Y esta vez»
B["c0"] = c0
B["logo"] = S(com) - .3
# vídeo de fondo: [id, inicio, fin, zoom inicial, zoom final]
B["v"] = [["t1", 0.0, S(y0) - .04, 1.0, 1.035],
          ["t2", S(y0) - .04, B["a"][0], 1.0, 1.04],
          ["t3", B["a"][0], B["a"][1], 1.0, 1.04],
          ["t4", B["a"][1], B["a"][2], 1.02, 1.08],
          ["t5", B["a"][2], B["lap2"][0] + .55, 1.0, 1.09],
          ["t6", B["f"][0], B["f"][1], 1.0, 1.04],
          ["t7", B["f"][1], c0 + .3, 1.0, 1.035]]
B["vn"] = {v[0]: len(list((Path(__file__).parent / "src/r6h" / v[0]).glob("*.jpg"))) for v in B["v"]}   # fotogramas por tramo
end = E(len(W) - 1) + TAIL
a, d, f = B["a"], B["d"], B["f"]
B["wt"] = {
    # ANTES: cada palabra del titular aparece cuando se dice
    "ha": [[round(S(i) - a[0], 3) for i in (men, lla - 1, lla, par - 1, par)],
           [round(S(i) - a[1], 3) for i in (la, vis, en_p, pap)],
           [round(S(i) - a[2], 3) for i in range(y1, pre + 1)]],
    "a5n": round(S(pre - 2) - a[2], 3),             # sello «NO SE PRESENTÓ» en «no se presenta»
    "d2r": round(S(res) - d[1], 3),                 # la IA responde
    "d4v": round(S(vis2) - d[3], 3),                # la visita aparece en la ficha
    "d1": [round(S(find("entra", con)) - d[0], 3), round(S(find("portal", con)) - d[0], 3), round(S(find("centralizado", con)) - d[0], 3)],
    "d5c": [round(S(i) - d[4], 3) for i in (ubi, dia, hor)],
    "hf": [[round(S(mc) - f[0], 3), round(S(mc + 1) - f[0], 3)], [round(S(i) - f[1], 3) for i in range(y6, vie + 1)]],
    # ¿Tu inmobiliaria sigue en el antes? | Pide tu demo gratis | y pasa al después.
    "c": [round(S(i) - c0, 3) for i in range(tu, len(W))],
}

# ---- efectos (t, sfx, dB, pan, hpf) ----
lg = B["logo"]
cues = [(0.0, "hit_soft_03", -12, 0, 0), (S(pie0), "hit_soft_01", -13, -.3, 0), (S(pie0) + .05, "glitch_wake", -19, -.3, 0),
        (S(y0) - .06, "whoosh_short_02", -14, .3, 400), (S(gan), "pop_dock_03", -11, .3, 0), (S(gan) + .05, "shimmer_glow", -15, .3, 600)]
# ANTES: cortes secos con golpe suave; vibración del móvil; papel; reloj y sello
cues += [(a[0], "hit_soft_03", -10, 0, 0), (a[0] + .02, "glitch_wake", -18, 0, 0),
         *[(S(men) + .1 + i * .28, ["click_ui_02", "pop_dock_02", "click_ui_03", "pop_dock_01"][i], -17, (i % 2 * 2 - 1) * .4, 0) for i in range(4)],
         (a[1], "whoosh_short_03", -15, -.3, 300), (S(pap), "click_mech_dial_1", -15, .2, 0),
         (a[2], "whoosh_low_wipe", -12, 0, 0), (a[2] + .5, "ticks_granular_calendar", -21, .3, 0),
         (S(pre - 2), "hit_metal_02", -12, 0, 0), (S(pre - 2) + .02, "hit_soft_03", -11, 0, 0)]
# del caos al orden: estallan los avisos y se recogen en el portátil
X0, X1 = B["x"]
cues += [*[(X0 + i * .055, ["pop_dock_01", "click_ui_01", "pop_dock_02", "click_ui_02", "pop_dock_03", "click_ui_03", "pop_dock_01", "click_ui_02"][i], -15, (i % 3 - 1) * .5, 0) for i in range(8)],
         (X1 - .3, "suck_reverse", -12, 0, 200)]
M0, M1, M2 = B["lap2"]
cues += [(M0, "whoosh_long_02", -13, 0, 250), (M0 + .4, "click_ui_02", -15, 0, 0), (M1 - .35, "riser_grid", -14, 0, 300),
         (M1 + .05, "whoosh_low_wipe", -8, 0, 0), (M2, "hit_soft_03", -9, 0, 0), (M2 + .05, "shimmer_glow", -14, 0, 600),
         (S(find("entra", con)) - .1, "whoosh_short_02", -13, 0, 400), (S(find("entra", con)) + .25, "pop_dock_01", -10, 0, 0),
         (S(find("entra", con)) + .3, "shimmer_glow", -16, 0, 600),
         *[(S(find("portal", con)) + i * .22, "click_ui_0" + str(1 + i % 3), -15, (i - 1.5) * .3, 0) for i in range(4)],
         (S(find("centralizado", con)), "hit_soft_02", -10, 0, 0), (S(find("centralizado", con)) + .05, "pop_dock_03", -14, 0, 0),
         (d[1], "pop_dock_01", -12, 0, 0), (d[1] + .5, "pop_dock_02", -13, -.4, 0), (d[1] + .5, "ticks_granular_curve", -20, 0, 0),
         (S(res), "pop_dock_03", -10, .4, 0), (S(res) + .05, "shimmer_glow", -15, .3, 600), (S(res) + .5, "click_mech_dial_2", -14, .4, 0),
         (d[2], "whoosh_short_03", -15, 0, 300), (d[2] + .3, "ticks_granular_calendar", -19, 0, 0), (d[2] + 1.0, "hit_soft_01", -14, 0, 0),
         (d[3] - .2, "whoosh_long_02", -14, 0, 250), (d[3] + .1, "pop_dock_01", -12, 0, 0), (S(vis2), "pop_dock_02", -12, .2, 0),
         (d[4] + .1, "pop_dock_03", -12, 0, 0),
         *[(S(i), f"click_ui_0{1 + j}", -14, (j - 1) * .4, 0) for j, i in enumerate((ubi, dia, hor))],
         (S(hor) + .5, "shimmer_glow", -14, 0, 600), (S(hor) + .5, "hit_soft_02", -12, 0, 0)]
# DESPUÉS en vídeo: corte luminoso al plano 4 y al 5
cues += [(f[0] - .08, "whoosh_long_01", -14, 0, 300), (f[0], "shimmer_glow", -15, 0, 600), (S(mc + 1), "hit_soft_02", -14, 0, 0),
         (f[1], "whoosh_short_04", -15, .2, 300), (S(vie), "pop_dock_02", -13, 0, 0), (S(vie) + .05, "shimmer_glow", -16, 0, 600)]
cues += [(c0 - .2, "whoosh_long_01", -14, 0, 300), (lg - .35, "riser_grid", -19, 0, 300), (lg + .05, "sub_drop", -11, 0, 0),
         (lg + .05, "logo_sting", -9, 0, 0), (S(com) - .05, "whoosh_short_04", -14, 0, 300), (S(com) + .3, "pop_dock_02", -9, 0, 0),
         (S(com) + .35, "shimmer_glow", -15, 0, 600)]
B["cues"] = [[round(x[0], 3), *x[1:]] for x in cues]
# música: ANTES con el filtro oscuro y hats (tensión), groove desde el DESPUÉS, acorde final bajo el logo
B.update({"s1": 0.0, "s2": M1, "s3": a[0], "s4": M1, "s5": M1, "s6": c0})


def rnd(v):
    if isinstance(v, float):
        return round(v, 3)
    if isinstance(v, list):
        return [rnd(x) for x in v]
    return v


B = {k: (v if k in ("wt", "cues", "vn") else rnd(v)) for k, v in B.items()}
B["end"] = round(end, 2)
tl = {"fps": 60, "duration": B["end"], "vo_offset": PRE, "beats": B,
      "note": f"build_timeline_r6h.py: VO {w_path} a atempo {TEMPO}; offset {PRE} s."}
json.dump(tl, open(out, "w"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in B.items() if k not in ("wt", "cues")}))
print("tramos de vídeo (s):", [(v[0], round(v[2] - v[1], 2)) for v in B["v"]])
